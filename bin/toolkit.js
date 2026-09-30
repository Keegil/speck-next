// Optional managed tools. No global install, PATH edit, hook, or automatic setup.
const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const { spawn, spawnSync } = require('child_process');

const OWNER = 'speck-next-toolkit-v1';
const MARKER = '.speck-next-tools.json';
const RECEIPT = '.speck-tool.json';
const LIMIT = 256 * 1024 * 1024;
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const exists = file => { try { return fs.lstatSync(file); } catch (e) { if (e.code === 'ENOENT') return null; throw e; } };
const inside = (base, file) => file === base || file.startsWith(base + path.sep);

function safeChain(file) {
  const absolute = path.resolve(file);
  let walked = path.parse(absolute).root;
  for (const part of absolute.slice(walked.length).split(path.sep).filter(Boolean)) {
    walked = path.join(walked, part);
    const entry = exists(walked);
    if (entry && entry.isSymbolicLink()) throw Error(`Refusing symlink cache path: ${walked}`);
  }
}

function readJson(file) {
  const entry = exists(file);
  if (!entry || !entry.isFile() || entry.isSymbolicLink()) throw Error(`Expected owned regular file: ${file}`);
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function ownedHome(home, create = false) {
  safeChain(home);
  const entry = exists(home);
  if (!entry) {
    if (!create) return false;
    fs.mkdirSync(home, { recursive: true, mode: 0o700 });
  } else if (!entry.isDirectory()) throw Error(`Tool cache is not a directory: ${home}`);
  const marker = path.join(home, MARKER);
  if (!exists(marker)) {
    if (!create || fs.readdirSync(home).length) throw Error(`Unowned tool cache; nothing changed: ${home}`);
    fs.writeFileSync(marker, JSON.stringify({ owner: OWNER }) + '\n', { flag: 'wx', mode: 0o600 });
  }
  if (readJson(marker).owner !== OWNER) throw Error(`Unowned tool cache; nothing changed: ${home}`);
  return true;
}

function command(file, args, options = {}) {
  const result = spawnSync(file, args, { encoding: 'utf8', timeout: 120000, maxBuffer: LIMIT, ...options });
  if (result.error || result.status !== 0)
    throw Error(`${path.basename(file)} failed: ${result.error?.message || (result.stderr || result.stdout || `exit ${result.status}`).toString().trim()}`);
  return result.stdout;
}

function environment() {
  return { ...process.env, DO_NOT_TRACK: '1', RTK_TELEMETRY_DISABLED: '1' };
}

function versionOf(binary, spec, env) {
  const args = spec.versionArgs || ['--version'];
  const output = command(spec.kind === 'npm' ? process.execPath : binary,
    spec.kind === 'npm' ? [binary, ...args] : args, { timeout: 10000, env }).trim();
  const escaped = spec.version.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return { output, matches: new RegExp(`(^|[^0-9])${escaped}($|[^0-9.])`).test(output) };
}

function toolDirectory(home, name, version) {
  if (!/^[a-z][a-z0-9-]*$/.test(name) || !/^[0-9][0-9A-Za-z.+-]*$/.test(version))
    throw Error('Unsafe tool name or version in manifest');
  const directory = path.join(home, name, version);
  safeChain(directory);
  return directory;
}

function managed(home, name, spec) {
  const directory = toolDirectory(home, name, spec.version);
  if (!exists(directory)) return null;
  const receipt = readJson(path.join(directory, RECEIPT));
  const binary = path.resolve(directory, receipt.executable || '');
  if (receipt.owner !== OWNER || receipt.name !== name || receipt.version !== spec.version ||
      !inside(directory, binary) || binary === directory) throw Error(`Invalid managed receipt: ${directory}`);
  safeChain(binary);
  if (!exists(binary)?.isFile() || sha(fs.readFileSync(binary)) !== receipt.binarySha256)
    throw Error(`Managed executable changed or missing: ${binary}. Remove and set up the toolkit again.`);
  return { directory, binary, receipt };
}

async function download(url, artifact, destination, allowHttp) {
  const parsed = new URL(url);
  if (parsed.protocol !== 'https:' && !(allowHttp && parsed.protocol === 'http:' && ['localhost', '127.0.0.1'].includes(parsed.hostname)))
    throw Error(`Download must use HTTPS: ${url}`);
  const response = await fetch(url, { signal: AbortSignal.timeout(60000) });
  if (!response.ok) throw Error(`Download failed (${response.status}): ${url}`);
  const chunks = []; let length = 0;
  for await (const chunk of response.body) {
    length += chunk.length;
    if (length > LIMIT) throw Error('Download exceeds 256 MiB limit');
    chunks.push(chunk);
  }
  const bytes = Buffer.concat(chunks);
  if (artifact.sha256) {
    if (sha(bytes) !== artifact.sha256) throw Error(`Integrity check failed: ${url}`);
  } else if (artifact.integrity && /^sha512-[A-Za-z0-9+/=]+$/.test(artifact.integrity)) {
    const actual = 'sha512-' + crypto.createHash('sha512').update(bytes).digest('base64');
    if (actual !== artifact.integrity) throw Error(`Integrity check failed: ${url}`);
  } else throw Error(`Missing supported integrity checksum: ${url}`);
  fs.writeFileSync(destination, bytes, { flag: 'wx', mode: 0o600 });
}

function safeMember(name) {
  if (!name || path.posix.isAbsolute(name) || /[\\\x00\r]/.test(name) || /^[A-Za-z]:/.test(name) || name.split('/').includes('..'))
    throw Error(`Unsafe archive member: ${JSON.stringify(name)}`);
}

function extractBinary(archive, artifact, destination) {
  if (artifact.format === 'executable') {
    fs.copyFileSync(archive, destination, fs.constants.COPYFILE_EXCL);
  } else {
    const zip = artifact.format === 'zip';
    if (!zip && artifact.format !== 'tar.gz') throw Error(`Unsupported archive format: ${artifact.format}`);
    safeMember(artifact.binary);
    if (/[*?\[\]{}]/.test(artifact.binary)) throw Error('Archive binary must be an exact member name');
    const listing = command(zip ? 'unzip' : 'tar', zip ? ['-Z1', archive] : ['-tzf', archive]);
    const members = listing.trimEnd().split('\n');
    members.forEach(safeMember);
    if (members.filter(name => name === artifact.binary).length !== 1)
      throw Error(`Archive must contain exactly one ${artifact.binary}`);
    const bytes = command(zip ? 'unzip' : 'tar', zip ? ['-p', archive, artifact.binary] : ['-xOzf', archive, '--', artifact.binary], { encoding: null });
    fs.writeFileSync(destination, bytes, { flag: 'wx', mode: 0o755 });
  }
  fs.chmodSync(destination, 0o755);
}

async function installOne(home, name, spec, platform, allowHttp) {
  const env = environment();
  const current = managed(home, name, spec);
  if (current) {
    if (!versionOf(current.binary, spec, env).matches) throw Error(`${name}: managed version does not match pin ${spec.version}`);
    console.log(`${name} ${spec.version}: already installed`);
    return;
  }
  const artifact = spec.kind === 'npm' ? spec : spec.platforms?.[platform];
  if (!artifact) throw Error(`${name}: unsupported platform ${platform}; existing tools remain available`);
  const directory = toolDirectory(home, name, spec.version);
  const parent = path.dirname(directory);
  fs.mkdirSync(parent, { recursive: true, mode: 0o700 });
  const stage = fs.mkdtempSync(path.join(home, `.stage-${name}-`));
  try {
    const archive = path.join(stage, spec.kind === 'npm' ? 'download.tgz' : 'download');
    await download(artifact.url, artifact, archive, allowHttp);
    let executable = 'tool';
    if (spec.kind === 'npm') {
      safeChain(path.join(home, '.npm-cache'));
      fs.writeFileSync(path.join(stage, 'package.json'), JSON.stringify({ private: true }) + '\n');
      command('npm', ['install', '--prefix', stage, '--no-audit', '--no-fund', '--omit=dev', archive], {
        cwd: stage, env: { ...env, npm_config_cache: path.join(home, '.npm-cache'), npm_config_update_notifier: 'false' }, timeout: 180000 });
      const pkg = readJson(path.join(stage, 'node_modules', spec.package, 'package.json'));
      const entry = typeof pkg.bin === 'string' ? pkg.bin : pkg.bin?.[spec.executable || name];
      if (!entry) throw Error(`${name}: npm package does not declare its executable`);
      const resolved = path.resolve(stage, 'node_modules', spec.package, entry);
      if (!inside(stage, resolved)) throw Error(`${name}: executable escapes managed package`);
      executable = path.relative(stage, resolved);
      safeChain(resolved);
    } else extractBinary(archive, artifact, path.join(stage, executable));
    const binary = path.join(stage, executable);
    if (!versionOf(binary, spec, env).matches) throw Error(`${name}: executable does not report pinned version ${spec.version}`);
    const lock = path.join(stage, 'package-lock.json');
    const receipt = { owner: OWNER, name, version: spec.version, platform, executable,
      source: artifact.url, integrity: artifact.sha256 || artifact.integrity,
      binarySha256: sha(fs.readFileSync(binary)), packageLockSha256: exists(lock) ? sha(fs.readFileSync(lock)) : null,
      installedAt: new Date().toISOString() };
    fs.writeFileSync(path.join(stage, RECEIPT), JSON.stringify(receipt, null, 2) + '\n');
    fs.unlinkSync(archive);
    safeChain(directory);
    if (exists(directory)) throw Error(`${name}: installation appeared while staging; nothing overwritten`);
    fs.renameSync(stage, directory);
    console.log(`${name} ${spec.version}: installed`);
  } finally {
    if (exists(stage)) fs.rmSync(stage, { recursive: true });
  }
}

function pathTool(name) {
  for (const directory of (process.env.PATH || '').split(path.delimiter)) {
    if (!directory) continue;
    const candidate = path.resolve(directory, name);
    try { fs.accessSync(candidate, fs.constants.X_OK); if (fs.statSync(candidate).isFile()) return candidate; } catch {}
  }
  return null;
}

function doctor(home, manifest) {
  let owned = false, error = null;
  try { owned = ownedHome(home); } catch (e) { error = e.message; }
  const tools = Object.entries(manifest.tools).map(([name, spec]) => {
    const result = { name, pinnedVersion: spec.version, managed: { status: 'missing' }, existing: null };
    if (owned) try {
      const item = managed(home, name, spec);
      if (item) {
        const probe = versionOf(item.binary, spec, environment());
        result.managed = { status: probe.matches ? 'ready' : 'version-mismatch', path: item.binary, version: probe.output };
      }
    } catch (e) { result.managed = { status: 'invalid', error: e.message }; }
    const external = pathTool(spec.executable || name);
    if (external) try { result.existing = { path: external, ...versionOf(external, { ...spec, kind: 'external' }, environment()), adopted: false }; }
    catch (e) { result.existing = { path: external, error: e.message, adopted: false }; }
    return result;
  });
  return { home, error, ready: !error && tools.every(tool => tool.managed.status === 'ready'), tools };
}

function remove(home, manifest) {
  if (!ownedHome(home)) { console.log('No managed toolkit installed.'); return; }
  for (const name of fs.readdirSync(home)) {
    if (name === MARKER || name === '.lock' || name === '.npm-cache') continue;
    if (!manifest.tools[name]) throw Error(`Refusing removal: unrecognized cache entry ${name}`);
    const parent = path.join(home, name); safeChain(parent);
    if (!fs.statSync(parent).isDirectory()) throw Error(`Refusing removal: unexpected entry ${parent}`);
    for (const version of fs.readdirSync(parent)) {
      const receipt = readJson(path.join(toolDirectory(home, name, version), RECEIPT));
      if (receipt.owner !== OWNER || receipt.name !== name || receipt.version !== version)
        throw Error(`Refusing removal: unowned version ${name}/${version}`);
    }
  }
  const retired = `${home}.retired-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
  fs.renameSync(home, retired);
  fs.rmdirSync(path.join(retired, '.lock'));
  console.log(`Managed toolkit retired to ${retired}. No PATH or project settings changed.`);
}

async function main(args, options = {}) {
  try {
    const manifest = options.manifest || require('./toolkit-manifest.json');
    const home = path.resolve(process.env.SPECK_NEXT_TOOL_HOME || path.join(os.homedir(), '.cache', 'speck-next', 'tools'));
    const platform = options.platform || `${process.platform}-${process.arch}`;
    const [action, ...rest] = args;
    if (['--help', '-h'].includes(action) && !rest.length) {
      console.log('Usage: tools setup | doctor [--json] | run <graft|rg|jq|ast-grep|rtk> -- <arguments> | remove\nSetup requires Node >=20 on macOS or Linux (arm64/x64). Tools stay in a managed cache; run never installs implicitly. Doctor probes tool versions; vendors may maintain their own caches.');
      return 0;
    }
    if (action === 'doctor' && (rest.length === 0 || rest.join(' ') === '--json')) {
      const report = doctor(home, manifest);
      console.log(JSON.stringify(report, null, 2));
      return report.ready ? 0 : 1;
    }
    if (action === 'run') {
      const [name, separator, ...toolArgs] = rest;
      const spec = manifest.tools[name];
      if (!spec || separator !== '--') throw Error('Usage: tools run <graft|rg|jq|ast-grep|rtk> -- <arguments>');
      if (!ownedHome(home)) throw Error('Toolkit is not installed. Run tools setup, or use an existing tool directly.');
      const item = managed(home, name, spec);
      if (!item) throw Error(`${name} ${spec.version} is not installed. Run tools setup, or use an existing tool directly.`);
      return await new Promise((resolve, reject) => {
        const child = spawn(spec.kind === 'npm' ? process.execPath : item.binary,
          spec.kind === 'npm' ? [item.binary, ...toolArgs] : toolArgs, { stdio: 'inherit', env: environment() });
        child.on('error', reject);
        child.on('exit', (code, signal) => resolve(code === null ? 128 + (os.constants.signals[signal] || 1) : code));
      });
    }
    if (!['setup', 'remove'].includes(action) || rest.length)
      throw Error('Usage: tools setup | doctor [--json] | run <tool> -- <arguments> | remove');
    if (action === 'setup') {
      if (Number((options.nodeVersion || process.versions.node).split('.')[0]) < 20)
        throw Error('Toolkit setup requires Node >=20. Existing tools and the ordinary method are unaffected.');
      if (!/^(darwin|linux)-(arm64|x64)$/.test(platform))
        throw Error(`Toolkit setup supports macOS/Linux arm64/x64; ${platform} is unsupported. Use existing tools directly.`);
      for (const [name, spec] of Object.entries(manifest.tools))
        if (spec.kind !== 'npm' && !spec.platforms?.[platform])
          throw Error(`${name}: unsupported platform ${platform}; nothing installed`);
    }
    if (action === 'remove' && !exists(home)) { console.log('No managed toolkit installed.'); return 0; }
    ownedHome(home, action === 'setup');
    const lock = path.join(home, '.lock');
    try { fs.mkdirSync(lock); } catch { throw Error(`Toolkit is busy, or a previous setup left ${lock}. Inspect it before retrying.`); }
    try {
      if (action === 'setup') for (const [name, spec] of Object.entries(manifest.tools))
        await installOne(home, name, spec, platform, options.allowHttp === true);
      else remove(home, manifest);
    } finally { if (exists(lock)) fs.rmdirSync(lock); }
    return 0;
  } catch (error) { console.error(`Toolkit: ${error.message}`); return 1; }
}

module.exports = { main };
if (require.main === module) main(process.argv.slice(2)).then(code => { process.exitCode = code; });
