<template>
    <div class="loader" :style="styleObject"></div>
</template>

<script>
export default {
    name: 'Loader',
    props: {
        size: {
            default: 150,
            type: Number
        }
    },
    computed: {
        styleObject: function() {
            let size = this.size + 'px';
            let off = (-this.size / 2) + 'px';
            return {
                'width': size,
                'height': size,
                'margin-top': off,
                'margin-left': off
            };
        }
    }
}
</script>

<style scoped>

.loader {
    border: 16px solid #f3f3f3; /* Light grey */
    border-top: 16px solid #303F9F; /* Blue */
    border-radius: 50%;
    animation: spin 1.2s linear infinite;
    position: absolute;
    top: 50%;
    left: 50%;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

</style>
