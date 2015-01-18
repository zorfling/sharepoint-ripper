SharePoint Ripper
=================

Screen scrape a SharePoint wiki to Markdown

This is largely intended for importing to Confluence with the [markdown-to-confluence-uploader](https://github.com/zorfling/markdown-to-confluence-uploader) or direct entry

This script requires a manual patch to Mechanize described [here](http://chriscolborne.com/sharepoint-scraping-with-python-mechanize-and-beautiful-soup/)

Copy `config.yml.dist` to `config.yml` and enter your details

|Option|Meaning|
|------|-------|
|username|Your SharePoint username|
|password|Your SharePoint password|
|sharepoint_url|The base domain of your SharePoint instance|
|wiki_base_url|The subdirectory of your particular wiki. This ripper will only process pages under this base_url|
|wiki_index|The index file of the wiki to start with. Assumes a big list of links to other pages under `wiki_base_url`|
|scrape_recursively|Whether to follow links and continue scraping or just the index page|
|content_div_id|The id of the innermost div that your pages all share|
|confluence_space_key|The key of your Confluence space|
|direct_confluence_entry|True if you'll copy and paste the resultant markdown straight into the wiki entry option of Confluence. False if you're using the [markdown-to-confluence-uploader](https://github.com/zorfling/markdown-to-confluence-uploader)|
|add_legacy_link|Whether to add a link to the bottom of each page linking back to the legacy SharePoint source page|
