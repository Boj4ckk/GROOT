<script setup>
</script>

<template>
    <br> 
    <div> <!-- page -->    

        <div> <!-- INTRO -->
            <h2>
                First AI-powered highlight-based content generator
            </h2>
            <h4>
                Tool that transforms your stream highlights into engaging, shareable clips
                optimized for any platform.
            </h4>
        </div> <!-- /> -->

        <div> <!-- BOUTON -->
            <div>
                <router-link to="studio" tag="button"> Try it for free </router-link> <!-- askip tag="button" c pour pas etre simplement un "<a>" mais un bouton mais je vois pas trop la dif la-->
            </div>
            <div>
                <p> No credit card needed </p>
            </div>
        </div> <!-- /> -->

        <div> <!-- DEMO (text + videos) -->
            <div> <!-- description -->
                <h3> AI-powered auto editing for perfect short videos </h3>
            </div>
            <div> <!-- videos -->
                <div> <!-- original highlight -->
                    <video src="" controls></video> <!-- controls c pour pouvoir mettre pause et tt -->
                    <p> Original highlight</p>
                </div>
                <div> <!-- Final video -->
                    <video src="" controls></video>
                    <p> Final video </p>
                </div>
            </div>
        </div> <!-- /> -->

        <div> <!-- plateformes -->
            <div> <!-- ecritures -->
                <h4> Automated posting to the platform of your choice </h4>
                <p> Automatically post your edited clips to following shorts platforms with no manual effort </p>
            </div>
            <div> <!-- logos -->
                <img src="" alt="tiktok">
                <img src="" alt="instagram"> 
                <img src="" alt="youtube">
            </div>
        </div> <!-- /> -->

    </div> <!-- page/> -->

</template>