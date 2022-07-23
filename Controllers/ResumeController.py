from discord.ext.commands import Context
from discord import Client
from Controllers.AbstractController import AbstractController
from Controllers.ControllerResponse import ControllerResponse
from Parallelism.ProcessManager import ProcessManager
from Parallelism.Commands import VCommands, VCommandsType


class ResumeController(AbstractController):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> ControllerResponse:
        processManager = ProcessManager()
        processContext = processManager.getRunningPlayerContext(self.guild)
        if processContext:
            # Send Resume command to be execute by player process
            command = VCommands(VCommandsType.RESUME, None)
            queue = processContext.getQueue()
            queue.put(command)

        return ControllerResponse(self.ctx)
