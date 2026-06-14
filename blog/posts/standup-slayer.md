---
title: "The Daily Standup Slayer: How This Lazy Manager Automated Everything (Except Meetings)"
date: "Sep 27, 2024"
category: automation
excerpt: "Python + Google Sheets + a cron job on AWS. The origin story of what eventually became DevTrack."
readTime: 4
tags: python,automation,management
source: devto
sourceUrl: https://dev.to/shashank_raj/the-daily-standup-slayer-how-this-lazy-manager-automated-everything-except-meetings-540
---

Let's face it, meetings are the beige walls of the productivity world. You know, endless loops of "what could have been" and "should have been" while everyone wrestles over a shrinking timeframe. Articles debunking their usefulness pile up like unread emails, but the charm of a good standup seems unshakeable for some (cough management cough).

So, here I was, a DevOps and system reliability magician, leading a team of Gen-Z developers who wouldn't fill a single tracker, let alone the holy trinity of email updates, fancy project management tools, and good ol' Excel.

We were deadlocked. Management craved updates everywhere, the devs rebelled against everything, and my job search was going nowhere fast.

Enter automation, the hero in this data-driven odyssey. What if the devs filled one glorious sheet and we used that sheet to conquer all? Talk about killing multiple birds with a few well-aimed scripts!

## Step 1: Building a Fortress of Simplicity

First, a template. Think Bunk Beds: easy to understand, enough room for (almost) everything, and compatible with most project management tools on the market. Google Sheets became my weapon of choice, thanks to their fantastic [Python API documentation](https://developers.google.com/sheets/api/quickstart/python).

## Step 2: Operation "Fill the Darn Sheet" (Good Luck!)

Next, convincing the devs to actually fill this daily. Let's just say my negotiation skills were put to the test. Think Jedi mind tricks, minus the lightsabers.

## Step 3: Let the Automation Take Flight

Now, the fun part! Imagine a "set it and forget it" solution, a tireless workhorse that runs once and keeps chugging along. Here's the Pythonic breakdown:

- **Grab the Credentials:** Authenticate with Google's servers once (thanks, refresh tokens!). This generates a magical `token.json` file, which holds the key to our automated kingdom.
- **Data Download:** Using the Python API, dive into Google Sheets and extract the data. Pandas filters for the latest updates.
- **Transformation Time:** Shape that data into a format that Jira, YouTrack, or your PM tool of choice understands.
- **Dissemination is Key:** The transformed data gets written to a JSON/CSV structure and a friendly email with the latest updates goes out to a distribution list. This file can be pasted directly into YouTrack/Jira, because CTRL+C and CTRL+V is the greatest human invention of all time for us mere programmers.

## A Few Caveats for the Cautious

The free tier of the Google Sheets API has limitations — think data on a diet, small and lightweight for optimal processing. To avoid polling the entire sheet every time, I used a Google Apps Script to sort the data by date. Knowing my developers wouldn't write essays in the update section (bless their Gen-Z brevity), I limited the data grab to 20 rows. We're talking targeted data extraction, not an epic download marathon.

## Deployment Shenanigans

With the Python API, I snatched 10 rows of data from the Google Sheet (defined in an environment variable, because who wants hardcoded stuff?). A Google account with the same project was set up to access [Gmail's send API](https://developers.google.com/gmail/api/guides/sending#python). Finally, some Docker magic streamlined deployment. The code, nestled snugly in a Docker container, landed on an AWS development instance where a cron job awaited its cue.

## The Grand Automation Symphony

- **End of Day:** Developers and I (reluctantly) fill out the template.
- **11 PM:** The Google Sheets Apps Script springs into action, sorting the entire sheet by date.
- **12:30 AM:** A cron job fires on the EC2 instance, launching a Docker container with the Python code.
- **The code does its thing:** reads the sheet, transforms the data, injects it into the PM tool, sends the update email, and sleeps soundly.
- Wake up to the sweet symphony of updates — or the lack thereof.

## The Inevitable Hiccups (and Dreams of Grandeur)

Let's be honest, the Apps Script can be flaky sometimes, forcing me to resort to manual sorting (a developer's burden, I know). Plus, I built a template for Jira integration, but full automation remains a future quest.

Maybe one day, I'll conquer API integrations with major PM tools, build a product, secure VC funding, and sell it to Atlassian. But hey, this is the Lazy Manager's Guide — for now.
