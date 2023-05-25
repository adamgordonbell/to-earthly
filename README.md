# to-earthly

## Run

Give OpenAI KEY:
```
echo "OPENAI_API_KEY=bla" > .env
```

Build docker image:
```
>earthly +docker
```
Run in a repo with a GHA workflow and get an Earthfile
```
docker run -v $(pwd):/input to-earthly
```



## ToDO
* Get React_simple working
* Strategy for SAVE ARTIFACT and SAVE ARTIFACT LOCALLY
* Test for docker compose
* docker it up and have people try it?

# Doesn't Handle
* matrix builds
* multi-lang monorepos ( try running separately for each one instead)
* repos with out github action workflows