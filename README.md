# Docker image builder

Builds your Docker images automatically, like magic. Good for handling common base images for all your projects, apps,
whatever.

## How do you use this then?

Well, we got 3 things you need to worry about:

1. General configuration in `settings.py`: Basically you need to set up your Docker hub username there to prefix all
   built images with the right name
2. Images and versions: First level of subdirectories in this repo is "images", as in the repository
   names (`username/<repository>`) for Docker hub. The subdirectories in that defines the "versions" - basically default
   tags for things to be built for that repository.
3. Additional tags: In `image/version/config.yaml` you can define additional tags for the built image, like `latest`, or
   whatever aliases you may want for it.

Afterwards you can either set this up on your own build pipelines with the commands:

```
poetry install
poetry run build
poetry run upload
```

## But what does it require?

You will need:

- [Docker CLI](https://docs.docker.com/get-docker/) >= 20.10.0 (we use `docker push --all-tags` to save some time)
- [Python](https://www.python.org/downloads/) >= 3.8 (maybe 3.7 or 3.6 works, but who cares, use at least 3.8)
- [Poetry](https://python-poetry.org/docs/#installation)

You could also just use the preconfigured GitHub workflows. If you do you'll just need to add `DOCKERHUB_USERNAME`
and `DOCKERHUB_TOKEN` secrets ("token" is a [personal access token](https://docs.docker.com/docker-hub/access-tokens/)) that will be used to log into your account for upload.

## Contributions

If you plan on contributing to the code ensure you use [pre-commit](https://pre-commit.com/#install) to guarantee the
code style stays uniform etc.

Also, please open an issue first to discuss the idea before sending a PR so that you know if it would be wanted or needs
re-thinking or if you should just make a fork for yourself.

## If I use this it means you own my things, right?

No. You are responsible for and own your own things. This code is licensed under the [BSD 3-clause license](LICENSE.md).

# Financial support

This project has been made possible thanks to [Cocreators](https://cocreators.ee) and [Lietu](https://lietu.net). You
can help us continue our open source work by supporting us on [Buy me a coffee](https://www.buymeacoffee.com/cocreators)
.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cocreators)
