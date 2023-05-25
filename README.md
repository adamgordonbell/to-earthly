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
* SAVE ARTIFACT and SAVE ARTIFACT LOCALLY examplles
* WITH DOCKER and docker compose examples

# Doesn't Handle

This doesn't handle so many things. All are possible to overcome with enough examples and enough context tokens.

* matrix builds
* multi-lang monorepos ( try running separately for each one instead)
* repos with out github action workflows