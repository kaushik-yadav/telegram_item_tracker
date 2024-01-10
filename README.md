
The project involves creating a Telegram bot using the Telegram API and Python to track and notify users about specific items in a designated channel. 
Users input their preferences, and the bot searches the channel for matching text. 
The bot maintains a "tracker.json" file to store the date and link of the most recently found item. 
It compares this data with newly discovered items, updating the file if the item is newer. 
Notifications are sent to a designated channel with the link and date of the newly available item.
If no new item is found or the date remains the same, the bot notifies with a "No new item found" message.
