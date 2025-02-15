# ruff: noqa: TCH003 TCH002 TCH001

from __future__ import annotations

from datetime import timedelta
from typing import Annotated, Literal

from pydantic import AliasChoices, BeforeValidator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

from crawlee._utils.models import timedelta_ms

__all__ = ['Configuration']


class Configuration(BaseSettings):
    """Configuration of the Crawler.

    Args:
        internal_timeout: Timeout for internal operations such as marking a request as processed.
        verbose_log: Allows verbose logging.
        default_storage_id: The default storage ID.
        purge_on_start: Whether to purge the storage on start.
    """

    model_config = SettingsConfigDict(populate_by_name=True)

    internal_timeout: Annotated[timedelta | None, Field(alias='crawlee_internal_timeout')] = None

    verbose_log: Annotated[bool, Field(alias='crawlee_verbose_log')] = False

    default_browser_path: Annotated[
        str | None,
        Field(
            validation_alias=AliasChoices(
                'apify_default_browser_path',
                'crawlee_default_browser_path',
            )
        ),
    ] = None

    disable_browser_sandbox: Annotated[
        bool,
        Field(
            validation_alias=AliasChoices(
                'apify_disable_browser_sandbox',
                'crawlee_disable_browser_sandbox',
            )
        ),
    ] = False

    log_level: Annotated[
        Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        Field(
            validation_alias=AliasChoices(
                'apify_log_level',
                'crawlee_log_level',
            )
        ),
        BeforeValidator(lambda value: str(value).upper()),
    ] = 'INFO'

    default_dataset_id: Annotated[
        str,
        Field(
            validation_alias=AliasChoices(
                'actor_default_dataset_id',
                'apify_default_dataset_id',
                'crawlee_default_dataset_id',
            )
        ),
    ] = 'default'

    default_key_value_store_id: Annotated[
        str,
        Field(
            validation_alias=AliasChoices(
                'actor_default_key_value_store_id',
                'apify_default_key_value_store_id',
                'crawlee_default_key_value_store_id',
            )
        ),
    ] = 'default'

    default_request_queue_id: Annotated[
        str,
        Field(
            validation_alias=AliasChoices(
                'actor_default_request_queue_id',
                'apify_default_request_queue_id',
                'crawlee_default_request_queue_id',
            )
        ),
    ] = 'default'

    purge_on_start: Annotated[
        bool,
        Field(
            validation_alias=AliasChoices(
                'apify_purge_on_start',
                'crawlee_purge_on_start',
            )
        ),
    ] = True

    write_metadata: Annotated[bool, Field(alias='crawlee_write_metadata')] = True

    persist_storage: Annotated[
        bool,
        Field(
            validation_alias=AliasChoices(
                'apify_persist_storage',
                'crawlee_persist_storage',
            )
        ),
    ] = True

    persist_state_interval: Annotated[
        timedelta_ms,
        Field(
            validation_alias=AliasChoices(
                'apify_persist_state_interval_millis',
                'crawlee_persist_state_interval_millis',
            )
        ),
    ] = timedelta(minutes=1)

    system_info_interval: Annotated[
        timedelta_ms,
        Field(
            validation_alias=AliasChoices(
                'apify_system_info_interval_millis',
                'crawlee_system_info_interval_millis',
            )
        ),
    ] = timedelta(seconds=1)

    max_used_cpu_ratio: Annotated[
        float,
        Field(
            validation_alias=AliasChoices(
                'apify_max_used_cpu_ratio',
                'crawlee_max_used_cpu_ratio',
            )
        ),
    ] = 0.95

    memory_mbytes: Annotated[
        int | None,
        Field(
            validation_alias=AliasChoices(
                'actor_memory_mbytes',
                'apify_memory_mbytes',
                'crawlee_memory_mbytes',
            )
        ),
    ] = None

    available_memory_ratio: Annotated[
        float,
        Field(
            validation_alias=AliasChoices(
                'apify_available_memory_ratio',
                'crawlee_available_memory_ratio',
            )
        ),
    ] = 0.25

    storage_dir: Annotated[
        str,
        Field(
            validation_alias=AliasChoices(
                'apify_local_storage_dir',
                'crawlee_storage_dir',
            ),
        ),
    ] = './storage'

    chrome_executable_path: Annotated[
        str | None,
        Field(
            validation_alias=AliasChoices(
                'apify_chrome_executable_path',
                'crawlee_chrome_executable_path',
            )
        ),
    ] = None

    headless: Annotated[
        bool,
        Field(
            validation_alias=AliasChoices(
                'apify_headless',
                'crawlee_headless',
            )
        ),
    ] = True

    xvfb: Annotated[
        bool,
        Field(
            validation_alias=AliasChoices(
                'apify_xvfb',
                'crawlee_xvfb',
            )
        ),
    ] = False

    @classmethod
    def get_global_configuration(cls) -> Self:
        """Retrieve the global instance of the configuration."""
        from crawlee import service_container

        if service_container.get_configuration_if_set() is None:
            service_container.set_configuration(cls())

        global_instance = service_container.get_configuration()

        if not isinstance(global_instance, cls):
            raise TypeError(
                f'Requested global configuration object of type {cls}, but {global_instance.__class__} was found'
            )

        return global_instance
