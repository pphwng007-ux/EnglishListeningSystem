class ListeningAppController {
    constructor() {
        this.form = document.getElementById("practice-form");
        this.audioPlayer = document.getElementById("audio-player");
        this.playBtn = document.getElementById("play-segment-btn");
        
        if (!this.form || !this.audioPlayer || !this.playBtn) return;

        this.lessonId = this.form.dataset.lessonId;
        this.attemptId = this.form.dataset.attemptId;
        this.segments = [];
        this.currentSegmentIndex = 0;
        this.isSubmitting = false;

        this.init();
    }
    async init() {
        this.bindEvents();
        await this.loadLessonSegments();
    }
    async loadLessonSegments() {
        try {
            const response = await fetch(`/api/lesson/${this.lessonId}/segments`);
            if (!response.ok) throw new Error("Không thể kết nối API tải dữ liệu bài học.");
            
            const data = await response.json();
            this.segments = data.segments;

            if (this.segments.length > 0) {
                this.setupCurrentSegment();
            }
        } catch (error) {
            console.error("Lỗi dòng dữ liệu:", error);
            alert("Đã xảy ra lỗi khi tải các phân đoạn âm thanh. Vui lòng tải lại trang.");
        }
    }
    setupCurrentSegment() {
        const activeSegment = this.segments[this.currentSegmentIndex];
        this.audioPlayer.src = activeSegment.audio_url;
        this.audioPlayer.load(); 
        this.updatePlayButtonVisual(false);
        this.highlightActiveSegmentUI(activeSegment.id);
    }

    bindEvents() {
        this.playBtn.addEventListener("click", () => this.toggleAudioPlayback());

        this.audioPlayer.addEventListener("ended", () => this.handleAudioSegmentEnded());
        this.audioPlayer.addEventListener("play", () => this.updatePlayButtonVisual(true));
        this.audioPlayer.addEventListener("pause", () => this.updatePlayButtonVisual(false));

        this.form.addEventListener("submit", (event) => this.handleFormSubmission(event));
    }

    toggleAudioPlayback() {
        if (this.audioPlayer.paused) {
            this.audioPlayer.play().catch(err => console.warn("Trình duyệt chặn tự động phát:", err));
        } else {
            this.audioPlayer.pause();
        }
    }


    updatePlayButtonVisual(isPlaying) {
        if (isPlaying) {
            this.playBtn.innerHTML = `
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>`;
            this.playBtn.title = "Tạm dừng";
        } else {
            this.playBtn.innerHTML = `
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z"></path>
                </svg>`;
            this.playBtn.title = "Phát đoạn nghe";
        }
    }

    
    highlightActiveSegmentUI(segmentId) {
        document.querySelectorAll(".segment-box-container").forEach(box => {
            box.classList.remove("ring-2", "ring-blue-500", "bg-white");
            box.classList.add("bg-gray-50");
        });

        const activeBox = document.getElementById(`box-seg-${segmentId}`);
        if (activeBox) {
            activeBox.classList.remove("bg-gray-50");
            activeBox.classList.add("ring-2", "ring-blue-500", "bg-white");
        }
    }

    
    handleAudioSegmentEnded() {
        const activeSegment = this.segments[this.currentSegmentIndex];
        const currentInput = document.getElementById(`input-seg-${activeSegment.id}`);
        
        if (currentInput) {
            currentInput.removeAttribute("disabled"); 
            currentInput.placeholder = "✍️ Mời bạn gõ cụm từ nghe được tại đây...";
            currentInput.focus(); 
        }

        if (this.currentSegmentIndex < this.segments.length - 1) {
            this.currentSegmentIndex++;
            setTimeout(() => this.setupCurrentSegment(), 800);
        } else {
            this.playBtn.disabled = true;
            this.playBtn.classList.add("opacity-50", "cursor-not-allowed");
            this.playBtn.innerHTML = `
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>`;
        }
    }

    async handleFormSubmission(event) {
        event.preventDefault(); 
        
        if (this.isSubmitting) return; 

        const submitBtn = this.form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = "⏳ Đang chấm điểm đa hình...";

        const answers = {};
        this.segments.forEach(seg => {
            const inputField = document.getElementById(`input-seg-${seg.id}`);
            answers[seg.id] = inputField ? inputField.value.trim() : "";
        });

        try {
            const response = await fetch(`/submit/${this.attemptId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    answers: answers,
                    duration: window.practiceDurationSeconds || 0
                })
            });

            if (!response.ok) throw new Error("Xử lý chấm điểm thất bại ở tầng Server.");

            const resultData = await response.json();
            window.location.href = resultData.redirect_url;

        } catch (error) {
            console.error("Lỗi gửi dữ liệu bài làm:", error);
            alert("Không thể gửi bài làm để chấm điểm. Vui lòng kiểm tra lại đường truyền mạng.");
            
            this.isSubmitting = false;
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    }
}
document.addEventListener("DOMContentLoaded", () => {
    window.listeningApp = new ListeningAppController();
});
