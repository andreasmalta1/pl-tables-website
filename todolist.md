# PL Tables website
- General CSS and page content/layout for all pages
  -- Group CSS as much as possible
- General JS for all pages
  -- Group JS as much as possible
  -- Use JS for error checking when sending data
  -- Error checking examples: dates make sense, no future dates, user inputs invalid year/season, show no matches played
- Page flow + CSS for seasons/manager/dates
- Highlight selected team when you select stint
- Add a page to see all the results (Might be a version 3 thing)
- Add admin API protection (API Key)
- Add function descriptions for better readability
- Modify readme.md
- Merge to master
- Buy domain for website
- Deploy using AWS


## Page Layout

- https://www.wix.com/website-template/view/html/1734?originUrl=https%3A%2F%2Fwww.wix.com%2Fwebsite%2Ftemplates&tpClick=view_button&esi=bbbae5b3-bba8-4d24-ba0d-fe39e1785318
- Index page to generate tables
- Navbar
 -- Highlight Chosen page
 -- Mobile
  --- Show nothing except links
  --- Highlight page currently on
  --- Cross to exit hamburger menu not showing
  --- Make sure nothing is pressable when shown hamburger menu
- Base JS
  -- Highlight page currently on
  -- Modify the hamburger menu so that when active, showing the menu in full page, highlight selected page, remove the footer and header, show the icons in the hamburger menu