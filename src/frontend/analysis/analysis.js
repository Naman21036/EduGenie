document.addEventListener(
    "DOMContentLoaded",
    () => {

        document
        .querySelectorAll(
            ".analysis-card"
        )
        .forEach(
            card => {

                card.addEventListener(
                    "mouseenter",
                    () => {

                        card.style.transform =
                        "translateY(-6px)";
                    }
                );

                card.addEventListener(
                    "mouseleave",
                    () => {

                        card.style.transform =
                        "translateY(0px)";
                    }
                );

            }
        );

    }
);