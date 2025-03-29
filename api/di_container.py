# import os
# from motor.motor_asyncio import AsyncIOMotorClient

# from dependency_injector.providers import (
#     Configuration,
#     Factory,
#     Singleton,
#     Resource,
# )
# from dependency_injector.containers import (
#     DeclarativeContainer,
#     WiringConfiguration,
# )



# class AppDiContainer(DeclarativeContainer):
#     wiring_config = WiringConfiguration(
#         packages=[
#             "app.main",
#             "app.routers.users",
#             "app.routers.resumes",
#         ]
#     )

#     # Configs
#     general_config = Configuration(strict=True)
#     general_config.from_dict(GeneralConfig().model_dump(exclude_unset=True))

#     mongo_client = Resource(
#         lambda: AsyncIOMotorClient(
#             host=os.environ.get("ATLAS_URI"),
#         )
#     )
#     database = Resource(lambda client: client[os.environ.get("DB_NAME")], mongo_client)