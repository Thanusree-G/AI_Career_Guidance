document.addEventListener('DOMContentLoaded', () => {
    
    // Elements
    const welcomeScreen = document.getElementById('welcome-screen');
    const chatInterface = document.getElementById('chat-interface');
    const startBtn = document.getElementById('start-btn');
    const chatMessages = document.getElementById('chat-messages');
    const optionsContainer = document.getElementById('options-container');
    const typingIndicator = document.getElementById('typing-indicator');

    // State
    const userResponses = {
        stage: '',
        stream: '',
        interest: '',
        goal: ''
    };

    let currentStep = 0;

    // Data structures for questions and dynamic options
    const questions = [
        {
            key: 'stage',
            text: "Hi there! I'm your AI Career Mentor. Let's find the best path for you. First, what is your current education level?",
            options: ["10th Class", "Intermediate", "Diploma", "B.Tech", "Degree"]
        },
        {
            key: 'stream',
            text: "Great! Based on your education, which stream are you currently in?",
            // Options are dynamic based on 'stage'
            getOptions: () => {
                const stage = userResponses.stage;
                if (stage === "10th Class") {
                    return ["General", "Not Decided Yet"];
                } else if (stage === "Intermediate") {
                    return ["MPC", "BiPC", "MEC", "CEC"];
                } else if (stage === "Diploma") {
                    return ["Computer Engineering", "Mechanical Engineering", "Civil Engineering", "Electrical Engineering", "Electronics & Communication Engineering", "Automobile Engineering"];
                } else if (stage === "B.Tech") {
                    return [
                        "Computer Science Engineering (CSE)", "Information Technology (IT)", 
                        "Artificial Intelligence & Machine Learning (AI & ML)", "Artificial Intelligence & Data Science (AI & DS)", 
                        "Electronics & Communication Engineering (ECE)", "Electrical & Electronics Engineering (EEE)", 
                        "Mechanical Engineering", "Civil Engineering", "Chemical Engineering"
                    ];
                } else if (stage === "Degree") {
                    return ["B.Sc Computer Science", "BCA", "B.Com", "BBA", "BA"];
                }
                return ["General"]; // Fallback
            }
        },
        {
            key: 'interest',
            text: "Awesome. Now, which field interests you the most?",
            options: [
                "Artificial Intelligence", "Software Development", "Data Science", 
                "Cyber Security", "Robotics", "Medicine", "Business", 
                "Government Jobs", "Design"
            ]
        },
        {
            key: 'goal',
            text: "Almost done! What is your ultimate career goal?",
            options: ["Job", "Business", "Higher Studies"]
        }
    ];

    // Start Conversation
    startBtn.addEventListener('click', () => {
        welcomeScreen.classList.add('hidden');
        chatInterface.classList.remove('hidden');
        askQuestion();
    });

    // Add a message to the chat UI
    function appendMessage(sender, text, isHtml = false) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        
        if (isHtml) {
            contentDiv.innerHTML = text;
        } else {
            contentDiv.textContent = text;
        }

        msgDiv.appendChild(contentDiv);
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Show typing indicator
    function showTyping() {
        optionsContainer.innerHTML = ''; // Clear options
        typingIndicator.classList.remove('hidden');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Hide typing indicator
    function hideTyping() {
        typingIndicator.classList.add('hidden');
    }

    // Ask the current question
    function askQuestion() {
        if (currentStep >= questions.length) {
            submitData();
            return;
        }

        const q = questions[currentStep];
        
        showTyping();
        
        // Simulate thinking delay
        setTimeout(() => {
            hideTyping();
            appendMessage('bot', q.text);
            
            // Render options
            const options = q.options ? q.options : q.getOptions();
            optionsContainer.innerHTML = '';
            
            options.forEach(opt => {
                const btn = document.createElement('button');
                btn.classList.add('option-chip');
                btn.textContent = opt;
                btn.addEventListener('click', () => handleOptionClick(q.key, opt));
                optionsContainer.appendChild(btn);
            });
            
            // Scroll options into view if necessary
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
    }

    // Handle user option selection
    function handleOptionClick(key, value) {
        // Save response
        userResponses[key] = value;
        
        // Clear options and show user message
        optionsContainer.innerHTML = '';
        appendMessage('user', value);
        
        // Move to next step
        currentStep++;
        askQuestion();
    }

    // Send data to backend and get recommendation
    function submitData() {
        showTyping();
        
        fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userResponses)
        })
        .then(response => response.json())
        .then(data => {
            hideTyping();
            
            const introText = "I have analyzed your profile and generated a personalized career roadmap!";
            appendMessage('bot', introText);
            
            const cardHtml = `
                <div class="recommendation-card" style="text-align: center;">
                    <h3 style="margin-bottom: 15px; color: var(--accent);">Your Dashboard is Ready</h3>
                    <p style="margin-bottom: 20px; color: #cbd5e1;">Click below to view your personalized skills, roadmap, and salary expectations.</p>
                    <button id="go-dashboard-btn" class="primary-btn pulse" style="margin: 0 auto;">View My Dashboard <i class="fa-solid fa-chart-line"></i></button>
                </div>
            `;
            
            // Add slight delay before showing the card
            setTimeout(() => {
                appendMessage('bot', cardHtml, true);
                
                // Add event listener to the dashboard button
                document.getElementById('go-dashboard-btn').addEventListener('click', () => {
                    window.location.href = '/dashboard';
                });

                // Add a reset button
                setTimeout(() => {
                    optionsContainer.innerHTML = '';
                    const resetBtn = document.createElement('button');
                    resetBtn.classList.add('option-chip');
                    resetBtn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Start Over';
                    resetBtn.addEventListener('click', () => {
                        window.location.reload();
                    });
                    optionsContainer.appendChild(resetBtn);
                }, 1000);
            }, 500);
        })
        .catch(err => {
            console.error('Error fetching recommendation:', err);
            hideTyping();
            appendMessage('bot', "Oops! Something went wrong while analyzing your profile. Please try again later.");
        });
    }
});
