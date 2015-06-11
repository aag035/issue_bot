# issue_bot
Simple Python Bot to accept emails sent to a specific email address and converts the content of the email into an issue on a 
specified Github repository. 

Currently configured with my personal Yahoo Account + GitHub username & token to create issue and Cron job is scheduled 
to run the script every 5 minutes.

Crontab command used : */5 * * * * python /{absolute_path_to_file}/issue_bot.py

Testing :

1. Send an e-mail with any subject & Content @ create_issue@yahoo.com
2. You can check the created issue @ https://github.com/aag035/issue_bot/issues (within 5 minutes)

