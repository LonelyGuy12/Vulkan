from discord.ext.commands import Context
from discord import Client
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Utils.Cleaner import Cleaner
from Parallelism.ProcessManager import ProcessManager


class NowPlayingHandler(AbstractHandler):
    def __init__(self, ctx: Context, bot: Client) -> None:
        super().__init__(ctx, bot)
        self.__cleaner = Cleaner()

    async def run(self) -> HandlerResponse:
        # Get the current process of the guild
        processManager = ProcessManager()
        processInfo = processManager.getRunningPlayerInfo(self.guild)
        if not processInfo:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)

        playlist = processInfo.getPlaylist()
        if playlist.getCurrentSong() is None:
            embed = self.embeds.NOT_PLAYING()
            return HandlerResponse(self.ctx, embed)

        if playlist.isLoopingOne():
            title = self.messages.ONE_SONG_LOOPING
        else:
            title = self.messages.SONG_PLAYING
        await self.__cleaner.clean_messages(self.ctx, self.config.CLEANER_MESSAGES_QUANT)

        info = playlist.getCurrentSong().info
        embed = self.embeds.SONG_INFO(info, title)
        return HandlerResponse(self.ctx, embed)