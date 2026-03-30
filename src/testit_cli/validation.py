import click
import validators


def validate_uuid(ctx, param, value):
    if value is None:
        return value
    if isinstance(value, (tuple, list)):
        if len(value) == 0:
            return value
        for item in value:
            if item is not None and not validators.uuid(item):
                raise click.BadParameter(
                    f'"{item}" uuid of {param.name} (3802f329-190c-4617-8bb0-2c3696abeb8f)'
                )
        return value
    if not validators.uuid(value):
        raise click.BadParameter(f'"{value}" uuid of {param.name} (3802f329-190c-4617-8bb0-2c3696abeb8f)')
    return value


def validate_url(ctx, param, value):
    if not validators.url(value):
        raise click.BadParameter(f'"{value}" url address of the Test IT instance (https://demo.testit.software)')

    if value.endswith("/"):
        return value[:-1]

    return value
