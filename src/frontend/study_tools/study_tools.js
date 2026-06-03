document.addEventListener(
    "DOMContentLoaded",
    () => {

        const cards =
        document.querySelectorAll(
            ".tool-card"
        );

        cards.forEach(
            card => {

                card.addEventListener(
                    "click",
                    () => {

                        cards.forEach(
                            c =>
                            c.classList.remove(
                                "selected"
                            )
                        );

                        card.classList.add(
                            "selected"
                        );

                    }
                );

            }
        );

    }
);