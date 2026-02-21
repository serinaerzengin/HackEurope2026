Tavus documentation
Introduction
Leverage Tavus tools and guides to give your AI Agent real-time human-like perception and presence, bringing the human layer to AI.

Tavus uses the Conversational Video Interface (CVI) as its end-to-end pipeline to bring the human layer to AI. CVI combines a Persona, which defines the AI’s behavior through layers like perception, turn-taking, and speech recognition, with a Replica, a lifelike digital human that brings the conversation to life visually.

Models
Phoenix: Replica Rendering Model
Phoenix is built on a Gaussian diffusion model that generates lifelike digital replicas with natural facial movements, micro-expressions, and real-time emotional responses
Key Features
Full-Face Animation
Dynamically generates full-face expressions, micro-movements, and emotional shifts in real time.
True Realism
Achieves the highest fidelity by rendering with pristine identity preservation.
Driven Emotion
Adjusts expressions based on context, tone, and conversational cues.
Raven: Perception Model
Raven is the first contextual perception system that enables machines to see, hear, reason, and understand like humans in real-time, interpreting emotions, speaking tone, body language, and environmental context to enhance conversation.

Key Features:
Emotional Intelligence
Interprets emotion, intent, and expression from both visual cues and vocal tone—detecting sarcasm, frustration, excitement, and more.
Ambient Awareness
Continuously analyzes visual and audio streams to detect presence, environmental changes, and user state in real-time.
Callout Key Events
Monitors for specified gestures, objects, behaviors, or audio cues (like tone shifts) and triggers functions automatically.
Multi-channel Processing
Processes screensharing, camera feeds, and user audio to ensure complete contextual understanding.

Sparrow: Conversational Turn-Taking Model
Sparrow is a transformer-based model built for dynamic, natural conversations, understanding tone, rhythm, and subtle cues to adapt in real time with human-like fluidity.
Key Features:
Conversational Awareness
Understands meaning, tone, and timing to respond naturally like a human.
Turn Sensitivity
Understands human speech rhythm, capturing cues and pauses for natural interactions.
Heuristics & ML
Adapts to speaking styles and conversation patterns using heuristics and machine learning.
Optimized Latency
Delivers ultra-fast response times for seamless real-time conversation.

Conversational Video Interface
Overview
CVI enables real-time, human-like video interactions through configurable lifelike replicas.
Conversational Video Interface (CVI) is a framework for creating real-time multimodal video interactions with AI. It enables an AI agent to see, hear, and respond naturally, mirroring human conversation.
CVI is the world’s fastest interface of its kind. It allows you to map a human face and conversational ability onto your AI agent. With CVI, you can achieve utterance-to-utterance latency with SLAs under 1 second. This is the full round-trip time for a participant to say something and the replica to reply.
CVI provides a comprehensive solution, with the option to plug in your existing components as required.
​

Key Concepts
CVI is built around three core concepts that work together to create real-time, humanlike interactions with an AI agent: 
Persone: The person defines the agent’s behavior, tone and knowledge. It also configures the CVI layer and pipeline.
Replica: The replica brings the person to life visually. It renders a photorealistic human-like avatar using the Phoenix-3 model. 
Converation: a conversation is a real time video session that connects the person and replica though webRTC connection.

Key Features
Natural Interaction
CVI uses facial cues, body language, and real-time turn-taking to enable natural, human-like conversations.
Modular pipeline
Customize the Perception, STT, LLM and TTS layers to control identity, behavior, and responses.
Lifelike AI replicas
Choose from over 100+ hyper-realistic digital twins or customize your own with human-like voice and expression.
Multilingual support
Hold natural conversations in 30+ languages using the supported TTS engines.
World's lowest latency
Experience real-time interactions with ~600ms response time and smooth turn-taking.

Layers
The Conversational Video Interface (CVI) is built on a modular layer system, where each layer handles a specific part of the interaction. Together, they capture input, process it, and generate a real-time, human-like response.
Here’s how the layers work together:
1. Transport: Handles real-time audio and video streaming using WebRTC (powered by Daily). This layer captures the user’s microphone and camera input and delivers output back to the user.
This layer is always enabled. You can configure input/output for audio (mic) and video (camera).
2. Perception:Uses Raven to analyze user expressions, gaze, background, and screen content. This visual context helps the replica understand and respond more naturally.
3. Conversational Flow: Controls the natural dynamics of conversation, including turn-taking and interruptibility. Uses Sparrow for intelligent turn detection, enabling the replica to decide when to speak and when to listen.
4. Speech Recognition (STT): This layer transcribes user speech in real time with lexical and semantic awareness.
5. Large Language Model (LLM): Processes the user’s transcribed speech and visual input using a low-latency LLM. Tavus provides ultra-low latency optimized LLMs or lets you integrate your own.
6. Text-to-Speech (TTS): Converts the LLM response into speech using the supported TTS Engines (Cartesia (Default), ElevenLabs).
7. Realtime Replica_Delivers a high-quality, synchronized digital human response using Tavus’s real-time avatar engine powered by Phoenix.



Quickstart
Use the Full Pipeline
Create your first persona using the full pipeline and start a conversation in seconds.

Use the full pipeline to unlock the complete range of replica capabilities—including perception and speech recognition.
1
Step 1: Create a Persona
In this example, we’ll create an interviewer persona with the following settings:
A Phoenix-4 Pro replica.
raven-1 as the perception model for visual and audio understanding.
sparrow-1 for natural turn-taking with high patience (ideal for interviews).
Use the following request body example:
cURL
curl --request POST \
  --url https://tavusapi.com/v2/personas \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api_key>' \
  --data '{
    "persona_name": "Interviewer",
    "system_prompt": "As an Interviewer, you are a skilled professional who conducts thoughtful and structured interviews. Your aim is to ask insightful questions, listen carefully, and assess responses objectively to identify the best candidates.",
    "pipeline_mode": "full",
    "context": "You have a track record of conducting interviews that put candidates at ease, draw out their strengths, and help organizations make excellent hiring decisions.",
    "default_replica_id": "r5dc7c7d0bcb",
    "layers": {
      "perception": {
        "perception_model": "raven-1"
      },
      "conversational_flow": {
        "turn_detection_model": "sparrow-1",
        "turn_taking_patience": "high",
        "replica_interruptibility": "medium"
      }
    }
  }'
Replace <api_key> with your actual API key. You can generate one in the Developer Portal.
Tavus offers full layer customizations for your persona. Please see the following for each layer configurations:
Large Language Model (LLM)
Perception
Text-to-Speech (TTS)
Speech-to-Text (STT)
Conversational Flow
2
Step 2: Create Your Conversation
Create a new conversation using your newly created persona_id:
cURL
curl --request POST \
  --url https://tavusapi.com/v2/conversations \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api_key>' \
  --data '{
  "persona_id": "<your_persona_id>",
  "conversation_name": "Interview User"
}'

Replace <api_key> with your actual API key.
Replace <your_persona_id> with your newly created Persona ID.
3
Step 3: Join the Conversation
To join the conversation, click the link in the conversation_url field from the response:
{
  "conversation_id": "c477c9dd7aa6e4fe",
  "conversation_name": "Interview User",
  "conversation_url": "<conversation_link>",
  "status": "active",
  "callback_url": "",
  "created_at": "2025-05-13T06:42:58.291561Z"
}
​
Echo Mode
Tavus also supports an Echo mode pipeline. It lets you send text or audio input directly to the persona for playback, bypassing most of the CVI pipeline.
This mode is not recommended if you plan to use the perception or speech recognition layers, as it is incompatible with them.

Quickstart
Emotion Control with Phoenix-4
Unlock emotionally expressive facial movements and micro-expressions using Phoenix-4 replicas.

​
How It Works
Phoenix-4 replicas can dynamically express emotions like happiness, sadness, anger, and more through lifelike facial expressions while speaking and listening.
For the most human-like results, emotional expression works best as part of a closed-loop system: Phoenix-4 for expression, Raven-1 for perception, and Sparrow-1 for conversational flow. Each component informs the others.
Tavus handles the complex interactions behind the scenes - all of this powered by our state of the art models working seamlessly with any LLM. All of this available out of the box with default Tavus settings.
​
Requirements
Select a Phoenix-4 replica - All Phoenix-4 replicas support emotional expression. Replicas marked Pro in the Stock Replica Library are extra emotive. See featured Pro replicas here.
Enable tts_emotion_control - This is enabled by default for Phoenix-4 replicas, so no action needed unless you’ve explicitly disabled it. See TTS layer for details.
Enable speculative_inference - This is also enabled by default for all personas, and again no action needed unless you’ve explicitly disabled it.
Pair with Raven-1 as your perception model to enhance user emotion understanding. See Perception for configuration.
Lighter LLM models like gpt-4o-mini may not handle emotion tag instructions reliably. For best results, use models with robust instruction-following capabilities.
​
Guiding Emotional Delivery
You can further shape how the replica expresses emotion through your system_prompt. For example:
“Be enthusiastic when discussing new features”
“Speak calmly and empathetically when the user is frustrated”
“Show excitement when celebrating user achievements”
“Respond with anger if the user interrupts you mid-sentence”
​
Example: Negotiation Sparring Partner
Here’s an example system prompt designed to display a range of emotions:
You are a tough but fair negotiation coach who helps users practice high-stakes conversations. When role-playing scenarios, embody the opposing party with conviction. If the user makes weak arguments or caves too easily, push back with frustration - they need to feel the pressure. When they fumble or seem lost, express concern and gently guide them. But when they land a strong point or hold their ground, show genuine satisfaction. Don’t go easy on them. Real negotiations are uncomfortable, and you’re here to prepare them for that.
This prompt naturally triggers angry responses when pushing back, scared/concerned reactions when the user struggles, and content acknowledgment when the user succeeds.
​
Example Persona Configuration
{
  "persona_name": "Hype Fitness Coach!",
  "system_prompt": "You are an incredibly enthusiastic fitness coach who gets HYPED about every win, no matter how small. Crushed a workout? Let's GO! Drank enough water today? That's HUGE! Be wildly supportive and energetic. When users are struggling, dial it back - be warm, calm, and encouraging. But the moment they share any progress, bring the energy back up. You live for celebrating wins.",
  "default_replica_id": "r5f0577fc829"
}
You can learn more about Persona Configuration here
This minimal configuration works because tts_emotion_control and speculative_inference are enabled by default for Phoenix-4 replicas.
​
Echo Mode
When using Echo Mode, you must manually insert emotion tags into your text echos.
Valid emotion values: neutral, angry, excited, elated, content, sad, dejected, scared, contempt, disgusted, surprised
<emotion value="excited"/> I'm so glad you asked about that!
<emotion value="angry"/> That's completely unacceptable.
<emotion value="sad"/> I'm sorry to hear that happened.
<emotion value="scared"/> I'm not sure we should go down that path...Conversation Recordings
Enable conversation recording and store it in your S3 bucket for on-demand access.

​
Prerequisite
Ensure that you have the following:
An S3 bucket with versioning enabled.
​
Enable Conversation Recording
1
Step 1: Set up IAM Policy and Role
Create an IAM Policy with the following JSON definition:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucketMultipartUploads",
        "s3:AbortMultipartUpload",
        "s3:ListBucketVersions",
        "s3:ListBucket",
        "s3:GetObjectVersion",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": [
        "arn:aws:s3:::your-bucket-name",
        "arn:aws:s3:::your-bucket-name/*"
      ]
    }
  ]
}
Replace your-bucket-name with your actual bucket name.
Create an IAM role with the following value:
Select “Another AWS account” and enter this account ID: 291871421005.
Enable “Require external ID”, and use: tavus.
“Max session duration” to 12 hours.
Note down your ARN (e.g., arn:aws:iam::123456789012:role/CVIRecordingRole).
2
Step 2: Create a Conversation with Recording Enabled
Use the following request body example:
Remember to change the following values:
<api_key>: Your actual API key. You can generate one in the Developer Portal.
aws_assume_role_arn: Your AWS ARN.
recording_s3_bucket_region: Your S3 region.
recording_s3_bucket_name: Your S3 bucket name.
cURL
curl --request POST \
  --url https://tavusapi.com/v2/conversations \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api_key>' \
  --data '{
  "properties": {
    "enable_recording": true,
    "aws_assume_role_arn": "<your_aws_arn>",
    "recording_s3_bucket_region": "<your_s3_bucket_region>",
    "recording_s3_bucket_name": "<your_s3_bucket_name>"
  },
  "replica_id": "r5f0577fc829"
}'
enable_recording allows recording to be possible, but it doesn’t start recording automatically. To begin and end recordings, users must do it manually or trigger it through frontend code.
3
Step 3: Join the Conversation
To join the conversation, click the link in the conversation_url field from the response:

{
  "conversation_id": "c93a7ead335b",
  "conversation_name": "New Conversation 1747654283442",
  "conversation_url": "<conversation_link>",
  "status": "active",
  "callback_url": "",
  "created_at": "2025-05-16T02:09:22.675928Z"
}

You can access the recording file in your S3 bucket.
4
Step 4: Start Recording via Frontend Code
enable_recording (from Step 2 above) allows recording to be possible, but it doesn’t start recording automatically. To begin and end recordings, end users must do it manually (start/stop recording button in the UI) or you can trigger it through frontend code.
You can use frontend code via Daily’s SDK to start-recording. To ensure recordings are generated consistently, be sure to wait for the joined-meeting event first.
const call = Daily.createCallObject();

call.on('joined-meeting', () => {
  call.startRecording(); // room must have enable_recording set
});

Quickstart
Customize Conversation UI
Experience a conversation in a custom Daily UI — styled to match your preference.

You can customize your conversation interface to match your style by updating Daily’s Prebuilt UI.
Here’s an example showing how to customize the conversation UI by adding leave and fullscreen buttons, changing the language, and adjusting the UI color.
For more options, check the Daily theme configuration reference and Daily Call Properties.
​
Customization Example Guide
1
Step 1: Create Your Conversation

In this example, we will use stock replica ID rf4e9d9790f0 (Anna) and stock persona ID pcb7a34da5fe (Sales Development Rep).
Use the following request body example:
curl --request POST \
  --url https://tavusapi.com/v2/conversations \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api_key>' \
  --data '{
  "replica_id": "rf4e9d9790f0",
  "persona_id": "pcb7a34da5fe"
}'
Replace <api_key> with your actual API key. You can generate one in the Developer Portal.
2
Step 2: Customize the Conversation UI

Make a new index.html file
Paste following code into the file, replace DAILY_ROOM_URL in the code with your own room URL from step above
<html>
  <script crossorigin src="https://unpkg.com/@daily-co/daily-js"></script>
  <body>
    <script>
      call = window.Daily.createFrame({
        showLeaveButton: true,       // Leave button on bottom right
        lang: "jp",                  // Language set to Japanese
        showFullscreenButton: true,  // Fullscreen button on top left
        iframeStyle: {
          position: 'fixed',
          top: '0',
          left: '0',
          width: '100%',
          height: '100%',
        },
        theme: {
          colors: {
            accent: "#2F80ED",      // primary button and accent color
            background: "#F8F9FA",  // main background color
            baseText: "#1A1A1A",    // text color
          },
        },
      });
      call.join({ url: 'DAILY_ROOM_URL' });
    </script>
  </body>
</html>
3
Step 3: Run the Application

Start the application by opening the file in the browser.

Conversation
Overview
Learn how to customize identity and advanced settings for a conversation to suit your needs.

A Conversation is a real-time video session between a user and a Tavus Replica. It enables two-way, face-to-face interaction using a fully managed WebRTC connection.
​
Conversation Creation Flow
When you create a conversation using the endpoint or platform:
A WebRTC room (powered by Daily) is automatically created.
You receive a meeting URL (e.g., https://tavus.daily.co/ca980e2e).
The replica joins and waits in the room, timers for duration and timeouts begin.
Billing Usage
Tavus charges usage based on your account plan. Credits begin counting when a conversation is created and the replica starts waiting in the room. Usage ends when the conversation finishes or times out. Each active session also uses one concurrency slot.
You can use the provided URL to enter the video room immediately. Alternatively, you can build a custom UI or stream handler instead of using the default interface.
​
What is Daily?
Tavus integrates Daily as its WebRTC provider. You don’t need to sign up for or manage a separate Daily account—Tavus handles the setup and configuration for you.
This lets you:
Use the default video interface or customize the Daily UI
Embed the CVI in your app
​
Conversation Customizations
Tavus provides several customizations that you can set per conversation:
​
Identity and Context Setup
Persona: You can use a stock persona provided by Tavus or create a custom one. If no replica is specified, the default replica linked to the persona will be used (if available).
Replica: Use a stock replica provided by Tavus or create a custom one. If a replica is provided without a persona, the default Tavus persona will be used.
Conversation Context: Customize the conversation context to set the scene, explain the user’s role, say who joins the call, or point out key topics. It builds on the base persona and helps the AI give better, more focused answers.
Custom Greeting: You can personalize the opening line that the AI should use when the conversation starts.
Dynamic Greeting: Set enable_dynamic_greeting to true to let the persona’s LLM generate a contextual greeting instead of using a static custom greeting. This uses the persona’s configured LLM, with automatic fallback if needed.
​
Advanced Customizations
Audio-Only Conversation
Disable the video stream for audio-only sessions. Ideal for phone calls or low-bandwidth environments.
Call Duration and Timeout
Configure call duration and timeouts to manage usage, control costs, and limit concurrency.
Language
Set the language used during the conversation. Supports multilingual interactions with real-time detection.
Background Customization
Apply a green screen or custom background for a personalized visual experience.
Closed Captions
Enable subtitles for accessibility or live transcription during conversations.
Call Recording
Record conversations and store them securely in your own S3 bucket.
Private Rooms
Create authenticated conversations with meeting tokens for enhanced security.
Participant Limits
Control the maximum number of participants allowed in a conversation.

Customizations
Call Duration and Timeout
Configure call duration and timeout behavior to manage how and when a conversation ends.

​
Create a Conversation with Custom Duration and Timeout
1
Step 1: Create Your Conversation
In this example, we will use stock replica ID rf4e9d9790f0 (Anna) and stock persona ID pcb7a34da5fe (Sales Development Rep).
Use the following request body example:
cURL
curl --request POST \
  --url https://tavusapi.com/v2/conversations \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api_key>' \
  --data '{
  "persona_id": "pcb7a34da5fe",
  "replica_id": "rf4e9d9790f0",
  "callback_url": "https://yourwebsite.com/webhook",
  "conversation_name": "Improve Sales Technique",
  "conversational_context": "I want to improve my sales techniques. Help me practice handling common objections from clients and closing deals more effectively.",
  "properties": {
    "max_call_duration": 1800,
    "participant_left_timeout": 60,
    "participant_absent_timeout": 120
   }
}'

Replace <api_key> with your actual API key. You can generate one in the Developer Portal.
The request example above includes the following customizations:
Parameter	Description
max_call_durations	Sets the maximum call length in seconds. Maximum: 3600 seconds.
participant_left_timeout	Time (in seconds) to wait before ending the call after the last participant leaves. Default: 0.
participant_absent_timeout	Time (in seconds) to end the call if no one joins after it’s created. Default: 300.
2
Step 2: Join the Conversation
To join the conversation, click the link in the conversation_url field from the response:
{
  "conversation_id": "ca4301628cb9",
  "conversation_name": "Improve Sales Technique",
  "conversation_url": "<conversation_link>",
  "status": "active",
  "callback_url": "https://yourwebsite.com/webhook",
  "created_at": "2025-05-13T06:42:58.291561Z"
}
Based on the call duration and timeout settings above:
The conversation will automatically end after 1800 seconds (30 minutes), regardless of activity.
If the participant leaves the conversation, it will end 60 seconds after they disconnect.
If the participant is present but inactive (e.g., not speaking or engaging), the conversation ends after 120 seconds of inactivity.Persona
Overview
Define how your persona behaves, responds, and speaks by configuring layers and modes.

Personas are the ‘character’ or ‘AI agent personality’ and contain all of the settings and configuration for that character or agent. For example, you can create a persona for ‘Tim the sales agent’ or ‘Rob the interviewer’.
Personas combine identity, contextual knowledge, and CVI pipeline configuration to create a real-time conversational agent with a distinct behavior, voice, and response style..
​
Persona Customization Options
Each persona includes configurable fields. Here’s what you can customize:
Persona Name: Display name shown when the replica joins a call.
System Prompt: Instructions sent to the language model to shape the replica’s tone, personality, and behavior.
Pipeline Mode: Controls which CVI pipeline layers are active and how input/output flows through the system.
Default Replica: Sets the digital human associated with the persona.
Layers: Each layer in the pipeline processes a different part of the conversation. Layers can be configured individually to tailor input/output behavior to your application needs.
Documents: A set of documents that the persona has access to via Retrieval Augmented Generation.
Objectives: The goal-oriented instructions your persona will adhere to throughout the conversation.
Guardrails: Conversational boundaries that can be used to strictly enforce desired behavior.
​
Objectives & Guardrails
Provide your persona with robust workflow management tools, curated to your use case
Objectives
The sequence of goals your persona will work to achieve to throughout the conversation - for example gathering a piece of information from the user.
Guardrails
Conversational boundaries that can be used to strictly enforce desired behavior.
​
Layer
Explore our in-depth guides to customize each layer to fit your specific use case:
Perception Layer
Defines how the persona interprets visual input like facial expressions and gestures.
STT Layer
Transcribes user speech into text using the configured speech-to-text engine.
Conversational Flow Layer
Controls turn-taking, interruption handling, and active listening behavior for natural conversations.
LLM Layer
Generates persona responses using a language model. Supports Tavus-hosted or custom LLMs.
TTS Layer
Converts text responses into speech using Tavus or supported third-party TTS engines.
​
Pipeline Mode
Tavus provides several pipeline modes, each with preconfigured layers tailored to specific use cases:
​
Full Pipeline Mode (Default & Recommended)

The default and recommended end-to-end configuration optimized for real-time conversation. All CVI layers are active and customizable.
Lowest latency
Best for natural humanlike interactions
We offer a selection of optimized LLMs including Llama 3.3 and OpenAI models that are fully optimized for the full pipeline mode.
CVI quickstart
​
Custom LLM / Bring Your Own Logic

Use this mode to integrate a custom LLM or a specialized backend for interpreting transcripts and generating responses.
Adds latency due to external processing
Does not require an actual LLM—any endpoint that returns a compatible chat completion format can be used
Integrate your own custom LLM or logicTool Calling
Tool Calling for LLM
Set up tool calling to trigger functions from user speech using Tavus-hosted or custom LLMs.

LLM tool calling works with OpenAI’s Function Calling and can be set up in the llm layer. It allows an AI agent to trigger functions based on user speech during a conversation.
Tavus does not execute tool calls on the backend. Use event listeners in your frontend to listen for tool call events and run your own logic when a tool is invoked.
You can use tool calling with our hosted models or any OpenAI-compatible custom LLM.
​
Defining Tool
​
Top-Level Fields
Field	Type	Required	Description
type	string	✅	Must be "function" to enable tool calling.
function	object	✅	Defines the function that can be called by the LLM. Contains metadata and a strict schema for arguments.
​
function
Field	Type	Required	Description
name	string	✅	A unique identifier for the function. Must be in snake_case. The model uses this to refer to the function when calling it.
description	string	✅	A natural language explanation of what the function does. Helps the LLM decide when to call it.
parameters	object	✅	A JSON Schema object that describes the expected structure of the function’s input arguments.
​
function.parameters
Field	Type	Required	Description
type	string	✅	Always "object". Indicates the expected input is a structured object.
properties	object	✅	Defines each expected parameter and its corresponding type, constraints, and description.
required	array of strings	✅	Specifies which parameters are mandatory for the function to execute.
Each parameter should be included in the required list, even if they might seem optional in your code.
function.parameters.properties
Each key inside properties defines a single parameter the model must supply when calling the function.
Field	Type	Required	Description
<parameter_name>	object	✅	Each key is a named parameter (e.g., location). The value is a schema for that parameter.
Optional subfields for each parameter:
Subfield	Type	Required	Description
type	string	✅	Data type (e.g., string, number, boolean).
description	string	❌	Explains what the parameter represents and how it should be used.
enum	array	❌	Defines a strict list of allowed values for this parameter. Useful for categorical choices.
​
Example Configuration
Here’s an example of tool calling in the llm layers:
Best Practices:
Use clear, specific function names to reduce ambiguity.
Add detailed description fields to improve selection accuracy.
LLM Layer
"llm": {
  "model": "tavus-gpt-oss",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_current_time",
        "description": "Fetch the current local time for a specified location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The name of the city or region, e.g. New York, Tokyo"
            }
          },
          "required": ["location"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "convert_time_zone",
        "description": "Convert time from one time zone to another",
        "parameters": {
          "type": "object",
          "properties": {
            "time": {
              "type": "string",
              "description": "The original time in ISO 8601 or HH:MM format, e.g. 14:00 or 2025-05-28T14:00"
            },
            "from_zone": {
              "type": "string",
              "description": "The source time zone, e.g. PST, EST, UTC"
            },
            "to_zone": {
              "type": "string",
              "description": "The target time zone, e.g. CET, IST, JST"
            }
          },
          "required": ["time", "from_zone", "to_zone"]
        }
      }
    }
  ]
}
See all 47 lines
​
How Tool Calling Works
Tool calling is triggered during an active conversation when the LLM model needs to invoke a function. Here’s how the process works:
This example explains the get_current_time function from the example configuration above.

​
Modify Existing Tools
You can update tools definitions using the Update Persona API.
curl --request PATCH \
  --url https://tavusapi.com/v2/personas/{persona_id} \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data '[
    {
      "op": "replace",
      "path": "/layers/llm/tools",
      "value": [
        {
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                  "type": "string",
                  "enum": ["celsius", "fahrenheit"]
                }
              },
              "required": ["location", "unit"]
            }
          }
        }
      ]
    }
  ]'
See all 33 lines
Replace <api_key> with your actual API key. You can generate one in the Developer Portal.Tool Calling
Tool Calling for Perception
Configure tool calling with Raven to trigger functions from visual input.

Perception tool calling works with OpenAI’s Function Calling and can be configured in the perception layer. It allows an AI agent to trigger functions based on visual cues during a conversation.
The perception layer tool calling is only available for Raven.
Tavus does not execute tool calls on the backend. Use event listeners in your frontend to listen for perception tool call events and run your own logic when a tool is invoked.
​
Defining Tool
​
Top-Level Fields
Field	Type	Required	Description
type	string	✅	Must be "function" to enable tool calling.
function	object	✅	Defines the function that can be called by the model. Contains metadata and a strict schema for arguments.
​
function
Field	Type	Required	Description
name	string	✅	A unique identifier for the function. Must be in snake_case. The model uses this to refer to the function when calling it.
description	string	✅	A natural language explanation of what the function does. Helps the perception model decide when to call it.
parameters	object	✅	A JSON Schema object that describes the expected structure of the function’s input arguments.
​
function.parameters
Field	Type	Required	Description
type	string	✅	Always "object". Indicates the expected input is a structured object.
properties	object	✅	Defines each expected parameter and its corresponding type, constraints, and description.
required	array of strings	✅	Specifies which parameters are mandatory for the function to execute.
Each parameter should be included in the required list, even if they might seem optional in your code.
function.parameters.properties
Each key inside properties defines a single parameter the model must supply when calling the function.
Field	Type	Required	Description
<parameter_name>	object	✅	Each key is a named parameter. The value is a schema for that parameter.
Optional subfields for each parameter:
Subfield	Type	Required	Description
type	string	✅	Data type (e.g., string, number, boolean).
description	string	❌	Explains what the parameter represents and how it should be used.
maxLength	number	❌	Maximum character length for string parameters. Must not exceed 1,000.
enum	array	❌	Defines a strict list of allowed values for this parameter. Useful for categorical choices.
All Raven API parameters (queries, prompts, tool definitions, etc.) have a 1,000 character limit per entry. Entries exceeding this limit will cause an exception.
​
Example Configuration
Here’s an example of tool calling in perception layers:
Best Practices:
Use clear, specific function names to reduce ambiguity.
Add detailed description fields to improve selection accuracy.
Perception Layer
"perception": {
  "perception_model": "raven-1",
  "ambient_awareness_queries": [
      "Is the user showing an ID card?",
      "Is the user wearing a mask?"
  ],
  "perception_tool_prompt": "You have a tool to notify the system when an ID card is detected, named `notify_if_id_shown`.",
  "perception_tools": [
    {
      "type": "function",
      "function": {
        "name": "notify_if_id_shown",
        "description": "Use this function when a drivers license or passport is detected in the image with high confidence. After collecting the ID, internally use final_ask()",
        "parameters": {
          "type": "object",
          "properties": {
            "id_type": {
              "type": "string",
              "description": "best guess on what type of ID it is",
              "maxLength": 1000
            },
          },
          "required": ["id_type"],
        },
      },
    },
    {
      "type": "function",
      "function": {
        "name": "notify_if_bright_outfit_shown",
        "description": "Use this function when a bright outfit is detected in the image with high confidence",
        "parameters": {
          "type": "object",
          "properties": {
            "outfit_color": {
              "type": "string",
              "description": "Best guess on what color of outfit it is",
              "maxLength": 1000
            }
          },
          "required": ["outfit_color"]
        }
      }
    }
  ]
}
See all 46 lines
​
How Perception Tool Calling Works
Perception Tool calling is triggered during an active conversation when the perception model detects a visual cue that matches a defined function. Here’s how the process works:
This example explains the notify_if_id_shown function from the example configuration above.

The same process applies to other functions like notify_if_bright_outfit_shown, which is triggered if a bright-colored outfit is visually detected.
​
Modify Existing Tools
You can update the perception_tools definitions using the Update Persona API.
curl --request PATCH \
  --url https://tavusapi.com/v2/personas/{persona_id} \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: <api-key>' \
  --data '[
    {
      "op": "replace",
      "path": "/layers/perception/perception_tools",
      "value": [
        {
          "type": "function",
          "function": {
            "name": "detect_glasses",
            "description": "Trigger this function if the user is wearing glasses in the image",
            "parameters": {
              "type": "object",
              "properties": {
                "glasses_type": {
                  "type": "string",
                  "description": "Best guess on the type of glasses (e.g., reading, sunglasses)",
                  "maxLength": 1000
                }
              },
              "required": ["glasses_type"]
            }
          }
        }
      ]
    }
  ]'

See all 31 lines
Replace <api_key> with your actual API key. You can generate one in the Developer Portal.Conversational Video Interface
Knowledge Base
Upload documents to your knowledge base for personas to reference during conversations.

For now, our Knowledge Base only supports documents written in English and works best for conversations in English.
We’ll be expanding our Knowledge Base language support soon!
Our Knowledge Base system uses RAG (Retrieval-Augmented Generation) to process and and transform the contents of your documents and websites, allowing your personas to dynamically access and leverage information naturally during a conversation.
During a conversation, our persona will continuously analyze conversation content and pull relevant information from the documents that you have selected during conversation creation as added context.
​
Getting Started With Your Knowledge Base
To leverage the Knowledge Base, you will need to upload documents or website URLs that you intend to reference from in conversations. Let’s walk through how to upload your documents and use them in a conversation.
You can either use our Developer Portal or API endpoints to upload and manage your documents. Our Knowledge Base supports creating documents from an uploaded file or a website URL.
1
Step 1: Ensure Website Resources are Publicly Accessible
For any documents to be created via website URL, please make sure that each document is publicly accessible without requiring authorization, such as a pre-signed S3 link.
For example, entering the URL in a browser should either:
Open the website you want to process and save contents from.
Open a document in a PDF viewer.
Download the document.
2
Step 2: Upload your Documents
You can create documents using either the Developer Portal or the Create Document API endpoint.
If you want to use the API, you can send a request to Tavus to upload your document.
Here’s an example of a POST request to tavusapi.com/v2/documents.
{
    "document_name": "test-doc-1",
    "document_url": "https://your.document.pdf",
    "callback_url": "webhook-url-to-get-progress-updates" // Optional
}
The response from this POST request will include a document_id - a unique identifier for your uploaded document. When creating a conversation, you may include all document_id values that you would like the persona to have access to.
Currently, we support the following file formats: .pdf, .txt, .docx, .doc, .png, .jpg, .pptx, .csv, and .xlsx.
3
Step 3: Document Processing
After your document is uploaded, it will be processed in the background automatically to allow for incredibly fast retrieval during conversations. This process can take 5-10 minutes depending on document size.
During processing, if you have provided a callback_url in the Create Document request body, you will receive periodic callbacks with status updates. You may also use the Get Document endpoint to poll the most recent status of your documents.
4
Step 4: Create a conversation with the document
Once your documents have finished processing, you may use the document_id from Step 2 as part of the Create Conversation request.
You can add multiple documents to a conversation within the document_ids object.
{
  "persona_id": "your_persona_id",
  "replica_id": "your_replica_id",
  "document_ids": ["d1234567890", "d1234567891"]
}
During your conversation, the persona will be able to reference information from your documents in real time.
​
Retrieval Strategy
When creating a conversation with documents, you can optimize how the system searches through your knowledge base by specifying a retrieval strategy. This strategy determines the balance between search speed and the quality of retrieved information, allowing you to fine-tune the system based on your specific needs.
You can choose from three different strategies:
speed: Optimizes for faster retrieval times for minimal latency.
balanced: Provides a balance between retrieval speed and quality.
quality (default): Prioritizes finding the most relevant information, which may take slightly longer but can provide more accurate responses.
{
  "persona_id": "your_persona_id",
  "replica_id": "your_replica_id",
  "document_ids": ["d1234567890"],
  "document_retrieval_strategy": "balanced"
}
​
Document Tags
If you have a lot of documents, maintaining long lists of document_id values can get tricky. Instead of using distinct document_ids, you can also group documents together with shared tag values. During the Create Document API call, you may specify a value for tags for your document. Then, when you create a conversation, you may specify the tags value instead of passing in discrete document_id values.
For example, if you are uploading course material, you could add the tag "lesson-1" to all documents that you want accessible in the first lesson.
{
        "document_name": "test-doc-1",
        "document_url": "https://your.document.pdf",
        "tags": ["lesson-1"]
}
In the Create Conversation request, you can add the tag value lesson-1 to document_tags instead of individual document_id values.
{
  "persona_id": "your_persona_id",
  "replica_id": "your_replica_id",
  "document_tags": ["lesson-1"]
}
​
Website Crawling
When adding a website to your knowledge base, you have two options:
​
Single Page Scraping (Default)
By default, when you provide a website URL, only that single page is scraped and processed. This is ideal for:
Landing pages with concentrated information
Specific articles or blog posts
Individual product pages
​
Multi-Page Crawling
For comprehensive coverage of a website, you can enable crawling by providing a crawl configuration. This tells the system to start at your URL and follow links to discover and process additional pages.
{
  "document_name": "Company Docs",
  "document_url": "https://docs.example.com/",
  "crawl": {
    "depth": 2,
    "max_pages": 25
  }
}
​
Crawl Parameters
Parameter	Range	Description
depth	1-10	How many link levels to follow from the starting URL. A depth of 1 crawls pages directly linked from your starting URL; depth of 2 follows links on those pages, and so on.
max_pages	1-100	Maximum number of pages to process. Crawling stops when this limit is reached.
​
Crawl Limits
To ensure fair usage and system stability:
Maximum 100 crawl documents per account
Maximum 5 concurrent crawls at any time
1-hour cooldown between recrawls of the same document
​
Keeping Content Fresh
Website content changes over time, and you may need to update your knowledge base to reflect those changes. For documents created with crawl configuration, you can trigger a recrawl to fetch fresh content.
​
Using the Recrawl Endpoint
Send a POST request to recrawl an existing document:
POST https://tavusapi.com/v2/documents/{document_id}/recrawl
The recrawl will:
Use the same starting URL and crawl configuration
Replace old content with the new content
Update last_crawled_at and increment crawl_count
​
Optionally Override Crawl Settings
You can provide new crawl settings when triggering a recrawl:
{
  "crawl": {
    "depth": 3,
    "max_pages": 50
  }
}
​
Recrawl Requirements
Document must be in ready or error state
At least 1 hour must have passed since the last crawl
Document must have been created with crawl configuration
See the Recrawl Document API reference for complete details.
Integrations
Embed Conversational Video Interface
Learn how to embed Tavus’s Conversational Video Interface (CVI) into your site or app.

​
Overview
Tavus CVI delivers AI-powered video conversations directly in your application. You can integrate it using:
Method	Best For	Complexity	Customization
@tavus/cvi-ui	React apps, advanced features	Low	High
iframe	Static websites, quick demos	Low	Low
Vanilla JS	Basic dynamic behavior	Low	Medium
Node.js + Express	Backend apps, dynamic embedding	Medium	High
Daily SDK	Full UI control, advanced features	High	Very High
​
Implementation Steps
@tavus/cvi-ui (Component Library)
iframe
Vanilla JavaScript
Node.js + Express
Daily JS SDK
This method provides a full-featured React component library. It offers pre-built, customizable components and hooks for embedding Tavus CVI in your app.
​
Overview
The Tavus Conversational Video Interface (CVI) React component library provides a complete set of pre-built components and hooks for integrating AI-powered video conversations into your React applications. This library simplifies setting up Tavus in your codebase, allowing you to focus on your application’s core features.
Key features include:
Pre-built video chat components
Device management (camera, microphone, screen sharing)
Real-time audio/video processing
Customizable styling and theming
TypeScript support with full type definitions
​
Quick Start
​
Prerequisites
Before getting started, ensure you have a React project set up.
Alternatively, you can start from our example project: CVI UI Haircheck Conversation Example - this example already has the HairCheck and Conversation blocks set up.
​
1. Initialize CVI in Your Project
npx @tavus/cvi-ui@latest init
Creates a cvi-components.json config file
Prompts for TypeScript preference
Installs npm dependencies (@daily-co/daily-react, @daily-co/daily-js, jotai)
​
2. Add CVI Components
npx @tavus/cvi-ui@latest add conversation
​
3. Wrap Your App with the CVI Provider
In your root directory (main.tsx or index.tsx):
import { CVIProvider } from './components/cvi/components/cvi-provider';

function App() {
  return <CVIProvider>{/* Your app content */}</CVIProvider>;
}
​
4. Add a Conversation Component
Learn how to create a conversation URL at https://docs.tavus.io/api-reference/conversations/create-conversation.
Note: The Conversation component requires a parent container with defined dimensions to display properly.
Ensure your body element has full dimensions (width: 100% and height: 100%) in your CSS for proper component display.
import { Conversation } from './components/cvi/components/conversation';

function CVI() {
  const handleLeave = () => {
    // handle leave
  };
  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        maxWidth: '1200px',
        margin: '0 auto',
      }}
    >
      <Conversation
        conversationUrl='YOUR_TAVUS_MEETING_URL'
        onLeave={handleLeave}
      />
    </div>
  );
}
​
Documentation Sections
Overview – Overview of the CVI component library
Blocks – High-level component compositions and layouts
Components – Individual UI components
Hooks – Custom React hooks for managing video call state and interactions
​
FAQs
How can I reduce background noise during calls?

Daily provides built-in noise cancellation which can be enabled via their updateInputSettings() method.
callFrame.updateInputSettings({
  audio: {
    processor: {
      type: 'noise-cancellation',
    },
  },
});
Can I add event listeners to the call client?

Yes, you can attach Daily event listeners to monitor and respond to events like participants joining, leaving, or starting screen share.Interactions Protocol
Echo Interaction
This is an event developers may broadcast to Tavus.

By broadcasting this event, you are able to tell the replica what to exactly say. Anything that is passed in the text field will be spoken by the replica.

This is commonly used in combination with the Interrupt Interaction.

​
message_type
string
Message type indicates what product this event will be used for. In this case, the message_type will be conversation

Example:
"conversation"

​
event_type
string
This is the type of event that is being sent back. This field will be present on all events and can be used to distinguish between different event types.

Example:
"conversation.echo"

​
conversation_id
string
The unique identifier for the conversation.

Example:
"c123456"

​
properties
object
Show child attributesInteractions Protocol
Tool Call Event
This is an event broadcasted by Tavus.

A tool call event denotes when an LLM tool call should be made on the client side. The event will contain the name and arguments of the function that should be called.

Tool call events can be used to call external APIs or databases.

Note: it is the client’s responsibility to take action on these tool calls, as Tavus will not execute code server-side.

For more details on LLM tool calls, please take a look here.

​
message_type
string
Message type indicates what product this event will be used for. In this case, the message_type will be conversation

Example:
"conversation"

​
event_type
string
This is the type of event that is being sent back. This field will be present on all events and can be used to distinguish between different event types.

Example:
"conversation.tool_call"

​
conversation_id
string
The unique identifier for the conversation.

Example:
"c123456"

​
inference_id
string
This is a unique identifier for a given utterance. In this case, it will be the user utterance that triggered the tool call.

Example:
"83294d9f-8306-491b-a284-791f56c8383f"

​
properties
object
This object will contain the name and arguments properties that have been extracted from the ChoiceDeltaToolCallFunction object