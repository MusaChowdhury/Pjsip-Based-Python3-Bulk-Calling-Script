# About
Pyhton3 script uses the pjsip library to call and play recorded audio to given numbers (CSV format).
<br>

# Use Case
The script can initiate calls to multiple numbers and play a predefined recording after the call is received.
<br>
This type of application can be useful for businesses that want to announce information to their customers.
<br>


# Features
<ul>
  <li> 
    <p>Filter unique numbers.</p>
  </li>
    <li> 
    <p>Try to call a number "N" times ( "N" can be set by the user) before ignoring the number.</p>
  </li>
    <li> 
    <p>After execution, the script gives a detailed report about "Answered Calls" and "Unanswered Calls".</p>
</ul>
<br>


# Steps To Use
Considering the script will be used on linux (ubuntu).
<ul>
  <li> 
    <p>Follow this <a href="https://github.com/mgwilliams/python3-pjsip">repository</a> to set up pjsip/pjsua for python3.</p>
  </li>
  <li> 
    <p>Check if "pjsua" installed correctly. </p>
  </li>
  <li> 
    <p>Create "call_list.csv" to a folder. Use delimiter "\n" while adding numbers(the numbers you want to call) to the csv file.</p>
  </li>
  <li> 
    <p>Change the audio file (must be wav format) name to "play.wav". "play.wav" will be played to numbers when call is received.</p>
  </li>
  <li> 
    <p>Copy "script.py" script to the working folder (working folder refers to where "play.wav" & "call_list.csv" files exist).</p>
  </li>
  <li> 
    <p>Update username, user password, sip server address inside the script before execution (variables are named relatively).</p>
  </li>
  <li> 
    <p>Open a terminal inside the folder. Run "python3 script.py" to execute the script.</p>
  </li>
</ul>

<br>


# Note
<ul>
  <li> 
    <p>While installing PJSIP carefully follow the steps. For first time it is better to use virtual machine.</p>
  </li>
    <li> 
    <p>Tested the script on Ubuntu Lts 20.04 ( Pjsip 2.10 & Python 3.8).</p>
  </li>
    <li> 
    <p>Tested with virtual numbers ( here virtual number referring such number which uses sip protocol).</p>
</ul>

<br>