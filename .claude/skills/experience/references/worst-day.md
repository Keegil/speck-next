# Test a consequential failure

Choose a failure that could materially change the judgment of this work. The suggestions below are optional; use those tied to the affected behavior, its uncertainty, and its consequences.

- **Permissions and privacy:** use the least-privileged relevant account and try a forbidden operation. Follow alternative entry points when the same protected data can reach them. For account switching or shared devices, look for another person's remaining data.
- **Persistence and concurrency:** compare stored state before and after the action. Try interruption or overlapping writes when the changed operation could lose or corrupt data.
- **Recovery:** cause a realistic dependency outage, timeout, invalid response, or failed write. Observe what the person can do next and whether their work survives.
- **Safety nets:** if relying on a check, rollback, or fail-closed path as evidence, deliberately trigger the failure it claims to handle. Keep destructive experiments in an appropriate disposable environment.
- **Inputs and data:** choose boundaries or realistic outliers that could invalidate the result. A threshold needs evidence from the relevant data; a fixture alone cannot establish a real-world distribution.
- **AI behavior:** run the shipped behavior under the relevant condition. Reading a prompt is not evidence that the model follows it.
- **Related defects:** after a finding, inspect the nearby paths sharing its mechanism, such as create/update or the reverse operation. Expand only where the finding gives a reason.
- **Evidence integrity:** if tests or judging logic changed, check whether the changed measurement can still expose the relevant defect.
- **Interface recovery:** try to finish the affected job after the failure. Inspect the actual rendering when visual containment or reachability matters.

Record the actions and observations that support your conclusion. Name consequential checks you could not execute as untested. Do not require unrelated attacks or a second persona merely to fill a roster.
