# Docker image builder

Builds your Docker images automatically, like magic. Good for handling common base
images for all your projects, apps, whatever.

This repository builds images to
[hub.docker.com/u/digitallivinginternational](https://hub.docker.com/u/digitallivinginternational)

## How do you use this then?

Well, we got 3 things you need to worry about:

1. General configuration in `settings.py`: Basically you need to set up your Docker hub
   username there to prefix all built images with the right name
2. Images and versions: First level of subdirectories in this repo is "images", as in
   the repository names (`username/<repository>`) for Docker hub. The subdirectories in
   that defines the "versions" - basically default tags for things to be built for that
   repository.
3. Additional tags: In `image/version/config.yaml` you can define additional tags for
   the built image, like `latest`, or whatever aliases you may want for it.

Afterwards you can either set this up on your own build pipelines with the commands:

```
poetry install
poetry run build_muliplatform
poetry run upload
poetry run scan
```

If you have images other images depend on, check out the `settings.PRIORITY_BUILDS`
option. Each list within it gets assigned a priority and can be built in parallel with
`--parallel` argument, the rest of the images will then get built after everything in
the `PRIORITY_BUILDS`.

```python
# Simple priority to a couple of images
PRIORITY_BUILDS = [
   "ubuntu-base/20.04",
   "ubuntu-base/22.04",
]
```

```python
# Tiered priorities of things that depend on earlier priorities
PRIORITY_BUILDS = [
  [
      "ubuntu-base/20.04",
      "ubuntu-base/22.04",
  ],
  [
      "python-base/ubuntu20.04-python3.9",
      "python-base/ubuntu22.04-python3.10",
  ]
]
```

## But what does it require?

You will need:

- [Docker CLI](https://docs.docker.com/get-docker/) >= 20.10.0 (we use
  `docker push --all-tags` to save some time)
- [Python](https://www.python.org/downloads/) >= 3.9
- [Poetry](https://python-poetry.org/docs/#installation)

You could also just use the preconfigured GitHub workflows. If you do you'll just need
to add a `DOCKERHUB_TOKEN` secret ("token" is a
[personal access token](https://docs.docker.com/docker-hub/access-tokens/)) that will be
used to log into your account for upload. This needs to be for the Docker hub user
configured in `settings.py`.

The `scan` command uses `trivy` which you will need installed on your system first.

## Multiplatform support

There are several technical restrictions when building images for multiple platforms
with `buildx`, such as that `buildx` can't find an image in local docker environment
(see notes in
[output](https://docs.docker.com/engine/reference/commandline/buildx_build/#output)
section of the docs). But it's possible to push base images right away to a docker
registry and then explicitly define this registry in `FROM` statements.

That's why there are 2 options to build images:

- `poetry run build` builds all images for the current platform only with `docker build`
  under the hood. It's suitable for local development of the images
- `poetry run build_multiplatform` builds all images using `docker buildx build` for
  linux/amd64 and linux/arm64. It requires extra setup (check
  [pipeline code](./.github/workflows/build-and-upload.yaml)) and is not recommended for
  local development

## Contributions

If you plan on contributing to the code ensure you use
[pre-commit](https://pre-commit.com/#install) to guarantee the code style stays uniform
etc.

Also, please open an issue first to discuss the idea before sending a PR so that you
know if it would be wanted or needs re-thinking or if you should just make a fork for
yourself.

## If I use this it means you own my things, right?

No. You are responsible for and own your own things. This code is licensed under the
[BSD 3-clause license](LICENSE.md).
