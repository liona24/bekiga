<template>
    <div class="loader"></div>
</template>

<script>
export default {
    name: 'Loader'
}
</script>

<style scoped>

.loader {
    border: 16px solid #f3f3f3; /* Light grey */
    border-top: 16px solid #303F9F; /* Blue */
    border-radius: 50%;
    width: 150px;
    height: 150px;
    animation: spin 1.2s linear infinite;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -75px;
    margin-left: -75px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

</style>
