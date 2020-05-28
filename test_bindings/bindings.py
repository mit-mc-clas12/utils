import htcondor
import classad

echo = htcondor.Submit({
    "request_cpus": "1",
    "request_memory": "128MB",
    "request_disk": "128MB",
})

schedd = htcondor.Schedd()
with schedd.transaction() as txn:
    cluster_id = echo.queue(txn, 1)
