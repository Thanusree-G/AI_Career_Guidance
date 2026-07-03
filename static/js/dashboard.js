document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Skill Progress Ring Animation ---
    const circularProgresses = document.querySelectorAll('.circular-progress');

    circularProgresses.forEach((cp, index) => {
        // Generate a random progress value between 10% and 90% for demo purposes
        // In a real app, this would be tied to user progress data
        const targetProgress = Math.floor(Math.random() * 80) + 10; 
        
        let currentProgress = 0;
        const progressValueElement = cp.querySelector('.progress-value');
        
        // Add a slight delay based on index for a nice cascading effect
        setTimeout(() => {
            const progressInterval = setInterval(() => {
                currentProgress++;
                progressValueElement.textContent = `${currentProgress}%`;
                
                // Update the conic gradient to fill the circle
                // The angle is (currentProgress / 100) * 360 degrees
                cp.style.background = `conic-gradient(var(--accent) ${currentProgress * 3.6}deg, rgba(255,255,255,0.1) 0deg)`;

                if (currentProgress >= targetProgress) {
                    clearInterval(progressInterval);
                }
            }, 15); // Speed of animation
        }, index * 200);
    });


    // --- 2. Interactive Roadmap Checkboxes ---
    const checkboxes = document.querySelectorAll('.roadmap-checkbox');

    // Load saved state from LocalStorage if available
    checkboxes.forEach((cb, index) => {
        const savedState = localStorage.getItem(`roadmap_step_${index}`);
        const timelineItem = cb.closest('.timeline-item');

        if (savedState === 'true') {
            cb.checked = true;
            timelineItem.classList.add('completed');
        }

        // Add event listener for changes
        cb.addEventListener('change', (e) => {
            const isChecked = e.target.checked;
            
            // Save to LocalStorage
            localStorage.setItem(`roadmap_step_${index}`, isChecked);

            // Update UI (change dot color)
            if (isChecked) {
                timelineItem.classList.add('completed');
            } else {
                timelineItem.classList.remove('completed');
            }
        });
    });
});
