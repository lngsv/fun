# Local forwarding

```shell
host1 $ py -m http.server 12345
# "localhost" is host1 for host1
# "bind: Cannot assign requested address" can be fixed with -4 flag but the warning doesn't affect forwarding
host2 $ ssh -L 12346:localhost:12345 host1
host2 $ curl localhost:12346
```

# Remote forwarding

```shell
host1 $ py -m http.server 12345
# "localhost" is host1 for host1
# "bind: Cannot assign requested address" can be fixed with -4 flag but the warning doesn't affect forwarding
host1 $ ssh -R 12346:localhost:12345 host2
host2 $ curl localhost:12346
```
