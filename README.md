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
 * Frustrated with hit or miss on understanding SAVE ARTIFACT
 * Maybe try https://learnprompting.org/docs/intermediate/chain_of_thought
* WITH DOCKER and docker compose examples Test for docker compose

# Doesn't Handle

This doesn't handle so many things. All are possible to overcome with enough examples and enough context tokens.

* matrix builds
* multi-lang monorepos ( try running separately for each one instead)
* repos with out github action workflows