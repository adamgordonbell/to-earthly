

## BUILD

#### Synopsis

* `BUILD [--platform <platform>] [--allow-privileged] <target-ref> [--<build-arg-name>=<build-arg-value>...]`

#### Description

The command `BUILD` instructs Earthly to additionally invoke the build of the target referenced by `<target-ref>`, where `<target-ref>` follows the rules defined by [target referencing](../guides/target-ref.md#target-reference). The invocation will mark any images, or artifacts saved by the referenced target for local output (assuming local output is enabled), and any push commands issued by the referenced target for pushing (assuming pushing is enabled).

{% hint style='info' %}
##### What is being output and pushed

In Earthly v0.6+, what is being output and pushed is determined either by the main target being invoked on the command-line directly, or by targets directly connected to it via a chain of `BUILD` calls. Other ways to reference a target, such as `FROM`, `COPY`, `WITH DOCKER --load` etc, do not contribute to the final set of outputs or pushes.

If you are referencing a target via some other command, such as `COPY` and you would like for the outputs or pushes to be included, you can issue an equivalent `BUILD` command in addition to the `COPY`. For example

```Dockerfile
my-target:
    COPY --platform=linux/amd64 (+some-target/some-file.txt --FOO=bar) ./
```

Should be amended with the following additional `BUILD` call:

```Dockerfile
my-target:
    BUILD --platform=linux/amd64 +some-target --FOO=bar
    COPY --platform=linux/amd64 (+some-target/some-file.txt --FOO=bar) ./
```

This, however, assumes that the target `+my-target` is itself connected via a `BUILD` chain to the main target being built. If that is not the case, additional `BUILD` commands should be issued higher up the hierarchy.
{% endhint %}

#### Options

##### `--<build-arg-key>=<build-arg-value>`

Sets a value override of `<build-arg-value>` for the build arg identified by `<build-arg-key>`.

The override value of a build arg may be a constant string

```
--SOME_ARG="a constant value"
```

or an expression involving other build args

```
--SOME_ARG="a value based on other args, like $ANOTHER_ARG and $YET_ANOTHER_ARG"
```

or a dynamic expression, based on the output of a command executed in the context of the build environment.

```
--SOME_ARG=$(find /app -type f -name '*.php')
```

Dynamic expressions are delimited by `$(...)`.

##### `--platform <platform>`

Specifies the platform to build on.

This flag may be repeated in order to instruct the system to perform the build for multiple platforms. For example

```Dockerfile
build-all-platforms:
    BUILD --platform=linux/amd64 --platform=linux/arm/v7 +build
```

For more information see the [multi-platform guide](../guides/multi-platform.md).

##### `--allow-privileged`

Same as [`FROM --allow-privileged`](#allow-privileged).

##### `--build-arg <build-arg-key>=<build-arg-value>` (**deprecated**)

This option is deprecated. Please use `--<build-arg-key>=<build-arg-value>` instead.

## VERSION

#### Synopsis

* `VERSION [options...] <version-number>`

#### Description

The command `VERSION` identifies which set of features to enable in Earthly while handling the corresponding Earthfile. The `VERSION` command is currently optional;
however will become mandatory in a future version of Earthly. When specified, `VERSION` must be the first command in the Earthfile.


| Version number | enabled features |
| --- | --- |
| `0.5` | _initial functionality will be preserved_ |
| `0.6` | `--use-copy-include-patterns --referenced-save-only --for-in --require-force-for-unsafe-saves --no-implicit-ignore` |

#### Options

Individual features may be enabled by setting the corresponding feature flag.
New features start off as experimental, which is why they are disabled by default.
Once a feature reaches maturity, it will be enabled by default under a new version number.

All features are described in [the version-specific features reference](./features.md).

## WITH DOCKER

#### Synopsis

```Dockerfile
WITH DOCKER [--pull <image-name>] [--load <image-name>=<target-ref>] [--compose <compose-file>]
            [--service <compose-service>] [--allow-privileged]
  <commands>
  ...
END
```

#### Description

The clause `WITH DOCKER` initializes a Docker daemon to be used in the context of a `RUN` command. The Docker daemon can be pre-loaded with a set of images using options such as `-pull` and `--load`. Once the execution of the `RUN` command has completed, the Docker daemon is stopped and all of its data is deleted, including any volumes and network configuration. Any other files that may have been created are kept, however.

The clause `WITH DOCKER` automatically implies the `RUN --privileged` flag.

The `WITH DOCKER` clause only supports the command [`RUN`](#run). Other commands (such as `COPY`) need to be run either before or after `WITH DOCKER ... END`. In addition, only one `RUN` command is permitted within `WITH DOCKER`. However, multiple shell commands may be stringed together using `;` or `&&`.

A typical example of a `WITH DOCKER` clause might be:

```Dockerfile
FROM earthly/dind:alpine
WORKDIR /test
COPY docker-compose.yml ./
WITH DOCKER \
        --compose docker-compose.yml \
        --load image-name:latest=(+some-target --SOME_BUILD_ARG=value) \
        --load another-image-name:latest=+another-target \
        --pull some-image:latest
    RUN docker run ... && \
        docker run ... && \
        ...
END
```

For more examples, see the [Docker in Earthly guide](../guides/docker-in-earthly.md) and the [Integration testing guide](../guides/integration.md).

For information on using `WITH DOCKER` with podman see the [Podman guide](../guides/podman.md)

{% hint style='info' %}
##### Note
For performance reasons, it is recommended to use a Docker image that already contains `dockerd`. If `dockerd` is not found, Earthly will attempt to install it.

Earthly provides officially supported images such as `earthly/dind:alpine` and `earthly/dind:ubuntu` to be used together with `WITH DOCKER`.
{% endhint %}

#### Options

##### `--pull <image-name>`

Pulls the Docker image `<image-name>` from a remote registry and then loads it into the temporary Docker daemon created by `WITH DOCKER`.

This option may be repeated in order to provide multiple images to be pulled.

{% hint style='info' %}
##### Note
It is recommended that you avoid issuing `RUN docker pull ...` and use `WITH DOCKER --pull ...` instead. The classical `docker pull` command does not take into account Earthly caching and so it would redownload the image much more frequently than necessary.
{% endhint %}

##### `--load <image-name>=<target-ref>`

Builds the image referenced by `<target-ref>` and then loads it into the temporary Docker daemon created by `WITH DOCKER`. The image can be referenced as `<image-name>` within `WITH DOCKER`.

`<target-ref>` may be a simple target reference (`+some-target`), or a target reference with a build arg `(+some-target --SOME_BUILD_ARG=value)`.

This option may be repeated in order to provide multiple images to be loaded.

The `WITH DOCKER --load` option does not mark any saved images or artifacts of the referenced target for local output, nor does it mark any push commands of the referenced target for pushing. For that, please use [`BUILD`](#build).

##### `--compose <compose-file>`

Loads the compose definition defined in `<compose-file>`, adds all applicable images to the pull list and starts up all applicable compose services within.

This option may be repeated, thus having the same effect as repeating the `-f` flag in the `docker-compose` command.

##### `--service <compose-service>`

Specifies which compose service to pull and start up. If no services are specified and `--compose` is used, then all services are pulled and started up.

This option can only be used if `--compose` has been specified.

This option may be repeated in order to specify multiple services.

##### `--platform <platform>`

Specifies the platform for any referenced `--load` and `--pull` images.

For more information see the [multi-platform guide](../guides/multi-platform.md).

##### `--allow-privileged`

Same as [`FROM --allow-privileged`](#allow-privileged).

##### `--build-arg <key>=<value>` (**deprecated**)

This option is deprecated. Please use `--load <image-name>=(<target-ref> --<build-arg-key>=<build-arg-value>)` instead.


## CMD (same as Dockerfile CMD)

#### Synopsis

* `CMD ["executable", "arg1", "arg2"]` (exec form)
* `CMD ["arg1, "arg2"]` (as default arguments to the entrypoint)
* `CMD command arg1 arg2` (shell form)

#### Description

The command `CMD` sets default arguments for an image, when executing as a container. It works the same way as the [Dockerfile `CMD` command](https://docs.docker.com/engine/reference/builder/#cmd).

## LABEL (same as Dockerfile LABEL)

#### Synopsis

* `LABEL <key>=<value> <key>=<value> ...`

#### Description

The `LABEL` command adds label metadata to an image. It works the same way as the [Dockerfile `LABEL` command](https://docs.docker.com/engine/reference/builder/#label).

## EXPOSE (same as Dockerfile EXPOSE)

#### Synopsis

* `EXPOSE <port> <port> ...`
* `EXPOSE <port>/<protocol> <port>/<protocol> ...`

#### Description

The `EXPOSE` command marks a series of ports as listening ports within the image. It works the same way as the [Dockerfile `EXPOSE` command](https://docs.docker.com/engine/reference/builder/#expose).

## ENV (same as Dockerfile ENV)

#### Synopsis

* `ENV <key> <value>`
* `ENV <key>=<value>`

#### Description

The `ENV` command sets the environment variable `<key>` to the value `<value>`. It works the same way as the [Dockerfile `ENV` command](https://docs.docker.com/engine/reference/builder/#env).

{% hint style='info' %}
##### Note
Do not use the `ENV` command for secrets used during the build. All `ENV` values used during the build are persisted within the image itself. See the [`RUN --secret` option](#run) to pass secrets to build instructions.
{% endhint %}

## ENTRYPOINT (same as Dockerfile ENTRYPOINT)

#### Synopsis

* `ENTRYPOINT ["executable", "arg1", "arg2"]` (exec form)
* `ENTRYPOINT command arg1 arg2` (shell form)

#### Description

The `ENTRYPOINT` command sets the default command or executable to be run when the image is executed as a container. It works the same way as the [Dockerfile `ENTRYPOINT` command](https://docs.docker.com/engine/reference/builder/#entrypoint).

## VOLUME (same as Dockerfile VOLUME)

#### Synopsis

* `VOLUME <path-to-target-mount> <path-to-target-mount> ...`
* `VOLUME ["<path-to-target-mount>", <path-to-target-mount> ...]`

#### Description

The `VOLUME` command creates a mount point at the specified path and marks it as holding externally mounted volumes. It works the same way as the [Dockerfile `VOLUME` command](https://docs.docker.com/engine/reference/builder/#volume).

## USER (same as Dockerfile USER)

#### Synopsis

* `USER <user>[:<group>]`
* `USER <UID>[:<GID>]`

#### Description

The `USER` command sets the user name (or UID) and optionally the user group (or GID) to use when running the image and also for any subsequent instructions in the build recipe. It works the same way as the [Dockerfile `USER` command](https://docs.docker.com/engine/reference/builder/#user).

## WORKDIR (same as Dockerfile WORKDIR)

#### Synopsis

* `WORKDIR <path-to-dir>`

#### Description

The `WORKDIR` command sets the working directory for following commands in the recipe. The working directory is also persisted as the default directory for the image. If the directory does not exist, it is automatically created. This command works the same way as the [Dockerfile `WORKDIR` command](https://docs.docker.com/engine/reference/builder/#workdir).

## HEALTHCHECK (same as Dockerfile HEALTHCHECK)

#### Synopsis

* `HEALTHCHECK NONE` (disable health checking)
* `HEALTHCHECK [--interval=DURATION] [--timeout=DURATION] [--start-period=DURATION] [--retries=N] CMD command arg1 arg2` (check container health by running command inside the container)

#### Description

The `HEALTHCHECK` command tells Docker how to test a container to check that it is still working. It works the same way as the [Dockerfile `HEALTHCHECK` command](https://docs.docker.com/engine/reference/builder/#healthcheck), with the only exception that the exec form of this command is not yet supported.

#### Options

##### `--interval=DURATION`

Sets the time interval between health checks. Defaults to `30s`.

##### `--timeout=DURATION`

Sets the timeout for a single run before it is considered as failed. Defaults to `30s`.

##### `--start-period=DURATION`

Sets an initialization time period in which failures are not counted towards the maximum number of retries. Defaults to `0s`.

##### `--retries=N`

Sets the number of retries before a container is considered `unhealthy`. Defaults to `3`.

## HOST (experimental)

{% hint style='info' %}
##### Note
The `HOST` command is experimental and must be enabled by enabling the `--use-host-command` flag, e.g.

```Dockerfile
VERSION --use-host-command 0.6
```
{% endhint %}

#### Synopsis

* `HOST <hostname> <ip>`

#### Description

The `HOST` command creates a hostname entry (under `/etc/hosts`) that causes `<hostname>` to resolve to the specified `<ip>` address.
<<Earthly Reference End>>