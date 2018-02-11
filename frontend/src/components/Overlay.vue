<template>
<div>
    <div class="overlay" :style="styleObject">
        <a href="javascript:void(0)" class="close" @click="$emit('close', { sucess: false })">&times;</a>
        <slot v-if="show"></slot>
    </div>
</div>
</template>

<script>
export default {
    name: 'Overlay',
    props: ['show'],
    computed: {
        styleObject: function() {
            return {
                height: this.show ? '100%' : '0%'
            }
        }
    }
}
</script>

<style>

.overlay {
    width: 100%;
    height: 0;
    position: fixed;
    z-index: 100;
    left: 0;
    top: 65px;
    background-color: rgba(209, 231, 255, 0.94);
    overflow-x: hidden;
    transition: 0.25s;
}

a.close {
    position: relative;
    top: 15px;
    left: 97%;
    font-size: 50px;
    text-decoration: none;
    color: #000;
}

</style>
