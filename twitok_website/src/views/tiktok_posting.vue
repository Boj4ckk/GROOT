<script setup>

const post = (video) => {
    // envoyer à l'api si download est coché, puis la video à envoyer 
}

</script>


<template>

<br> Yo t'es la pour poster sur tiktok automatiquement ? 

<video src="../media/tiktok_format.mp4"></video>

<div>
    <p>Export plateform</p>
    <form action="">
        <label for="download"> Download </label>
        <input type="checkbox" id="donwload" name="donwload">
        <input type="button" value="EXPORT" @click="posting(video)">
    </form>
</div> 

</template>