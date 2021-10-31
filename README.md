# text-mining

Please read the [instructions](instructions.md).

# SMS Spam Classification

## Project Overview
My project is a spam detection and classification project based on a sms spam collection dataset.
The data I used comes from a public set of SMS labeled messages that have been collected by University of Campinas, Brazil.
The collection has 747 manually extracted SMS spam messages and 4827 randomly chosen legitimate (ham) messages.
To accomplish the target of spam detection, I did some preprocess to the raw data and then compute the word frequencies separately for ham and spam messages.

## Implementation
My project has three major components: data process, compute and inference. 
The data process component will read data from file to a ham list and a spam list,
and they can also do some preprocess stuffs to the raw string data, which will generate a list of word list.
Every word in the word list will be used for frequency computing.

The compute components will produce a frequencies dictionary for every single word.
And the ham and spam word frequencies is our major basis for spam message classification.
As for the inference components, it will compare the input message with ham and spam frequencies word by word and decide whether it's a spam message.

There are some little tiny components to fit those major components all together, like split data to train and test and top-k statistical view etc.
The train-test split is one major future in my project. 
Cause if you compute and test the performance of my project with the same data, then the result might be unconvincing.

## Results
I got a accuracy of 0.973 at spam detection and the data preprocess has made a big difference at this brilliant result.
During preprocess stage, I deleted the punctuations in the text, lowered every word,
translated numbers to some specific flag, recognized the web url.
I spent a long time observing the raw data and drew some conclusion on the differences between ham and spam messages.
These trivial operations have provided a huge progress on my classification accuracy (0.912 -> 0.973).

Although the accuracy on spam detection is quite considerable, the classification on original ham text is relatively unsatisfying (0.825).
In practice, the detection of spam message should never block the normal daily communication.
So I add a extra threshold at the inference stage, which tends to believe a sms message to be a normal message.
While setting the threshold to 1.1, I got the ham detection accuracy to 0.878 (0.053↑) and spam detection accuracy to 0.953 (0.020↓).
And the total accuracy came to 0.888 from 0.841 (0.047↑).

## Reflection
In general, my project went well in ham/spam classification and i did got a good plan for testing.
But there's still improvement to be done, more data preprocess, text similarity computation, data visualization with text clustering and etc.
Also, I'm not confident that my project would work well outside the SMS Spam collection data, maybe I should try the nltk.classify package later.
