const audio = document.querySelector(".audio-player");
const replayButton = document.querySelector("[data-replay]");
const transcriptButton = document.querySelector("[data-toggle-transcript]");
const transcript = document.querySelector(".transcript");
const form = document.querySelector("[data-practice-form]");

if (replayButton && audio) {
    replayButton.addEventListener("click", () => {
        audio.currentTime = 0;
        audio.play();
    });
}

if (transcriptButton && transcript) {
    transcriptButton.addEventListener("click", () => {
        const isHidden = transcript.hasAttribute("hidden");
        transcript.toggleAttribute("hidden", !isHidden);
        transcriptButton.textContent = isHidden ? "An transcript" : "Hien transcript";
    });
}

if (form) {
    form.addEventListener("submit", (event) => {
        const groups = [...form.querySelectorAll("fieldset")];
        const missing = groups.some((group) => {
            return !group.querySelector("input[type='radio']:checked");
        });

        if (missing) {
            event.preventDefault();
            alert("Ban hay chon dap an cho tat ca cau hoi truoc khi nop bai.");
        }
    });
}
