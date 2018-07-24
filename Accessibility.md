[TOC]

# Accessibility Testing For All Systems and Checklist
Created By: Sarah Watts and Scott Heggen  
Version: 0  
Link to Google Doc: https://docs.google.com/document/d/1ru_5tNl0NFIq443DcMxYoFfNb4OXnO26HLHwI13vfdE/edit?usp=sharing

## Purpose

Anywhere from 15 to 20% percent of people are disabled. If a website is not accessible then there are 
literally **millions** of people that are unable to access your website. If you have a website you want to 
make sure that everyone can us it, because you are proud of it, you want to make sure that it works. 
It's also a legal issue. The college would be open to lawsuits if there's website in not accessible.
Website accessibility isn't that hard either, it just adds a couple of steps to your coding routine. 
 
Before you issue a pull request that touches the front end (HTML, JAVASCRIPT, CSS) in any way, 
you **MUST** go through accessibility testing. If you code fails at any time during the "Beginner" portion of 
the checklist you must fix it before you're pull request can be accepted. You're pull request will not be accepted if it fails at at
any point during the "Beginner" portion of the checklist

## Background

A lot of you don't know how to do website accessibility testing. So below is a link of a video run through of a basic accessibility test. 

**How to do accessibility checks:**  

* https://youtu.be/cOmehxAU_4s 

One of the thing you will need to download is a screen reader. If you have a PC you will be using NVDA, 
if you have a MAC you can just built in voice over. NVDA is a good screen reader, and I've been told by blind friend that 
it's better than the paid one anyway. Anyway, below are links that should help you learn how to work the screen readers 
since there are shortcuts that you need to use, because you want to navigate the sight a way a blind person would. 

**NVDA Download Link**  

* https://www.nvaccess.org/download/

**NVDA Basics:**  
  
* https://youtu.be/Jao3s_CwdRU  
* https://webaim.org/articles/nvda/   
* https://youtu.be/Vx1vSd5uYS8  


**Voice Over Basics:**  
  
* https://youtu.be/5R-6WvAihms   

Screen readers are more compatible with certain browsers. For NVDA you need to use Firefox for testing and for Voice Over you need to use safari. 

**Browsers: **  
  
* Firefox  
* Google Chrome  
* Internet Explorer/Edge  
* Safari (Mac Only)  

**Browser Extension (Works for both Chrome and Firefox):**  
  
* AXE: https://www.deque.com/axe  

Here is a playlist that is contains about 20 videos that are really helpful teaching web accessibility: 
https://www.youtube.com/redirect?v=fGLp_gfMMGU&event=video_description&redir_token=VV0dWg1lvH1jnVJ5M_6JfXTj-6h8MTUyODIxNDMyOUAxNTI4MTI3OTI5&q=https%3A%2F%2Fgoo.gl%2F06qEUW

Below is the checklist that pertains to all the websites. It is based on The Website Accessibility Guidelines version 2.0 created by the W3C. 
There are three levels: Beginner, Intermediate, and Advanced. We are not expecting to reach the Advanced level, 
right now we just want to make sure that every website at least fits the Beginner level and then work up from there.  

**In order for your page to meet the minimum you need to have all the items on the Beginner checklist.**  

## Checklists   

### Beginner   

1. Are there text alternative for non-text content that is not purely for decoration? **(Correct Answer: Yes, N/A)**  
2. Is there any video present on the page? **If so,**    
    1. Is there an alternative to video-only and audio-only content? **(Correct Answer: Yes)**   
    2. Are captions provided for any video? **(Correct Answer: Yes)**
    3. Is there a second alternative for video with audio? **(Correct Answer: Yes)**     
3. Does the page have a logical structure? **(Correct Answer: Yes)**  
4. Is everything presented in meaningful order? **(Correct Answer: Yes)**
5. Is there more than one sense used for instructions? **(Correct Answer: Yes)**
6. Is there any audio on the page? **If so,**    
    1. Does the audio automatically play? **(Correct Answer: No)**    
7. Does the presentation of any material rely solely on color? **(Correct Answer: No)**  
8. Does the focus tab order make logical sense? **(Correct Answer: Yes)**  
9. Does anything mouse operable not get keyboard focus? **(Correct Answer: Yes)**  
10. Is there any keyboard traps? **(Correct Answer: No)**  
11. When navigating using a keyboard, does any hidden item get focus? **(Correct Answer: No)**  
12. Is there anything that is time limited? **If so,**    
    1. Can time be adjusted for the user? **(Correct Answer: Yes)**    
13. Is there any moving content?  **If so,**    
    1. Is the user provided with controls for moving said content? **(Correct Answer: Yes)**  
14. Is there any content that flashes more than three time per second? **(Correct Answer: No)** 
15. Is a "Skip to Content" link provided? **(Correct Answer: Yes, N/A)** 
16. Are the title pages helpful and clear? **(Correct Answer: Yes)**  
17. Is everything presented in a logical order? **(Correct Answer: Yes)**  
18. Is every link's purposed clear from it's context? **(Correct Answer: Yes)**  
19. Is there any link that says "Read More", "Click here" or something of that nature? **(Correct Answer: No)**  
20. Does the page have a lang attribute? **(Correct Answer: Yes)**  
21. Do any elements change when they receive focus, excluding focus ring? **(Correct Answer: No)**  
22. Do any elements change when they receive input? **(Correct Answer: No)**  
23. Are any input errors clearly identified (not using color only)? **(Correct Answer: Yes)**  
24. Are elements labeled, in a clear, logical, and meaningful way? **(Correct Answer: Yes)**  
25. Are form elements labeled correctly? **(Correct Answer: Yes)**  
26. Are instructions given in accessible ways? **(Correct Answer: Yes)**  
27. Are there any major code errors? **(Correct Answer: No)**  
28. Are the correct aria tags used (such as name, role, and value)? **(Correct Answer: Yes)**  
29. Is the contrast ratio between text and background at least 4.5:1? **(Correct Answer: Yes)**  
30. Are any images of text used to convey information (Logos do not count)? **(Correct Answer: No)**  

## Intermediate  

31. Is there any live video? If so,  
32. 































