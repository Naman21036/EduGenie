document.addEventListener(
    "DOMContentLoaded",
    () => {

        const counters =
        document.querySelectorAll(
            ".counter"
        );

        counters.forEach(
            counter => {

                const target =
                Number(
                    counter.dataset.target
                );

                let count = 0;

                const increment =
                target / 50;

                const updateCounter =
                () => {

                    if(
                        count < target
                    ){

                        count += increment;

                        counter.innerText =
                        Math.ceil(
                            count
                        );

                        requestAnimationFrame(
                            updateCounter
                        );
                    }

                    else{

                        counter.innerText =
                        target;
                    }
                };

                updateCounter();
            }
        );
    }
);