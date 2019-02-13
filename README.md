# Show of Screens

Show of hands is amethod used to hold impromptu votes in a crowd. To determine a vote we insruct those who are in favor of sth. to raise their hands. Raised hands are then counted to determine the result.

This repo contains code to implement an automatically counted show of hands. A count is obtained by taking a picture of the crowd, with those in favor of a proposal raising their mobile phones screens. The software then counts phone screens in the image in order to determine the vote.

# Usage

Place an image file named `phones.jpg` showing a crowd with phones.

```
$ pip3 install -r requirements.txt
$ python phones.py phones.jpg
Found 64 phones
```

