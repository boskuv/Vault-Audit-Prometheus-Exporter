# Vault-Audit-Prometheus-Exporter

https://developer.hashicorp.com/vault/tutorials/monitoring/monitor-telemetry-audit-splunk
https://developer.hashicorp.com/vault/tutorials/monitoring/usage-metrics

type: The type of an audit entry, either "request" or "response". For a successful request, there will always be two events. The audit log event of type "response" will include the "request" structure, and will have all the same data as a request entry. For successful requests you can do all your searching on the events with type "response".

request.path: The path of an API request (request|response).mount_type: The type of the mount that handles this request or response.

request.operation: The operation performed (eg read, create, delete...) auth: The authentication information for the caller
    .entity_id: If authenticated using an auth backend, the entity-id of the user/service
    .role_name: Depending on auth backend, the role name of the user/service

error: Populated (non-empty) if the response was an error, this field contains the error message.

response.data: In the case of a successful response, many will contain a data field corresponding to what was returned to the caller. Most fields will be masked with HMAC when sensitive.

./raft.sh start
export VAULT_ADDR=http://127.0.0.1:8200
get root token
vault audit enable file file_path=//home/user/Projects/vault/Vault-Audit-Prometheus-Exporter/scripts/vault_audit.log

