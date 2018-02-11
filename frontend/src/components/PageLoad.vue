<template>
  
</template>

<script>
export default {
    name: 'PageLoad',
    props: ['value'],
    data: function() {
        return {
            protocol: '',
        }
    },
    watch: {
        protocol: function() {
            this.$emit('input', this.protocol);
        }
    },
    created: function() {
        this.protocol = this.value;
    },
}
</script>

<style>

</style>
