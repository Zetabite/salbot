from discord.ext import commands
import logging
import discord

# COPIED FROM ANOTHER BOT, DEFINITELY DOESNT WORK AND NEEDS LOADS OF FIXES

@commands.command(pass_context=True)
@commands.has_any_role("Member", "Private Chat Access", "OG Role That Has No Purpose", "Moderator", "Administrator")
async def help(self, ctx, *, command_or_category: Optional[str] = None):
    """See the help menu."""
    if command_or_category is None:
        embed = ctx.embed(
            title="Help",
            description="Help for salbot")

        commanded_cogs = [
            cog for cog in self.bot.cogs if len(self.bot.cogs[cog].get_commands()) > 0]
        
        for name in commanded_cogs:
            cog = self.bot.cogs[name]
            if len(cog.get_commands()) > 0:
                name = cog.qualified_name
                strings = []
                for cmd in cog.get_commands():
                    if await cmd.can_run(ctx):
                        strings.append(f"`{cmd.name}`")

                if len(strings) == 0:
                    break

                value = ", ".join(strings)
                embed.add_field(name=name, value=value)
        
        embed.set_footer(text="support.help.footer")
    else:
        cmd = self.bot.get_command(command_or_category)
        
        if cmd is not None:
            await cmd.can_run(ctx)
            
            embed = ctx.embed(
                title="support.help.viewing", command=self.bot.command_prefix + cmd.qualified_name))

            embed.add_field(name="support.help.usage", value=f"{self.bot.command_prefix}{cmd.qualified_name} {cmd.signature}".strip(), inline=False)

            if len(cmd.aliases) > 0:
                embed.add_field(name="support.help.aliases", value=", ".join(cmd.aliases), inline=False)

            if hasattr(cmd, 'commands'):
                embed.add_field(name="support.help.subcommands", value=", ".join(scmd.name for scmd in cmd.commands), inline=False)

            if hasattr(cmd, 'required_permissions'):
                embed.add_field(
                    name="support.help.permissions",
                    value=", ".join("permission." + Permission.LABELS[perm])
                                    for perm in cmd.required_permissions))

            try:
                help = cmd.qualified_name.replace(' ', '.') + ".help_text"
                assert help != cmd.qualified_name.replace(' ', '.') + ".help_text"
            except AssertionError:
                help = "support.help.help.not_found"
            
            embed.add_field(name="support.help.help", value=help, inline=False)

            try:
                example = cmd.qualified_name.replace(' ', '.') + ".example_text"
                assert example != cmd.qualified_name.replace(' ', '.') + ".example_text"
            except AssertionError:
                example = "support.help.example.not_found"
            
            embed.add_field(name="support.help.example", value=example, inline=False)

            embed.set_footer(text="support.help.arguments")
        else:
            cog = self.bot.get_cog(command_or_category)
            if cog is not None:
                embed = ctx.embed(
                    title=cog.qualified_name,
                    description="support.help.viewing", command=cog.qualified_name))

                embed.add_field(name="support.help.commands", value=", ".join(cmd.name for cmd in cog.get_commands()), inline=False)
            else:
                embed = ctx.error("support.help.not_found")

    await embed.send()

        
def setup(bot):
    bot.add_command(help)
