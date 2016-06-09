```
 ________   _______ .______        _______  __       __  .__   __.   _______ 
|       /  |   ____||   _  \      /  _____||  |     |  | |  \ |  |  /  _____|
`---/  /   |  |__   |  |_)  |    |  |  __  |  |     |  | |   \|  | |  |  __  
   /  /    |   __|  |      /     |  | |_ | |  |     |  | |  . `  | |  | |_ | 
  /  /----.|  |____ |  |\  \----.|  |__| | |  `----.|  | |  |\   | |  |__| | 
 /________||_______|| _| `._____| \______| |_______||__| |__| \__|  \______| 
```

Usage
=====

To upvote as `USERID`:

    zergling up -u USERID -t PERMALINK

To downvote as `USERID`:

    zergling down -u USERID -t PERMALINK

To run in a container:

    docker run --env-file=ENVS kevinjqiu/zergling up -u USERID -t PERMALINK
