# to-earthly

## Run from pre-built image

```
docker run --rm -it --name my_container -v $(pwd):/input agbell/to-earthly
```


## Run using your own OpenAI key

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
docker run --rm -it --name my_container -v $(pwd):/input to-earthly
```

## ToDO

* get dockerfile support working
* get matrix builds working
* WITH DOCKER and docker compose examples Test for docker compose

# Doesn't Handle

This doesn't handle so many things. All are possible to overcome with enough examples and enough context tokens.