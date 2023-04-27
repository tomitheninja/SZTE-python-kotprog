from discord import ui
import discord

class ProfileViewEditBtn(ui.View):
    
    def __init__(self, label: str = "Szerkesztés", modal: ui.Modal = None):
        super().__init__()
        btn = ui.Button(label=label, style=discord.ButtonStyle.primary)
        
        async def callback(interaction: discord.Interaction):
            await interaction.response.send_modal(modal)
        
        btn.callback = callback
        self.add_item(btn)