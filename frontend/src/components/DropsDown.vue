<template>
<div style="display: inline-block"
    @keydown.down="next"
    @keydown.up="previous"
    @keydown.enter="selectActive()"
    @keydown.tab="selectActive()"
    >
    <slot></slot>
    <div class="dropdown">
        <span v-for="(item, idx) in items"
            :key="'item-' + idx"
            class="dropdown-item" :class="{ 'dropdown-active': active === idx }"
            @mouseover="() => active = idx"
            @mousedown="selectActive()">
            {{ item.repr }}
        </span>
    </div>
</div>
</template>

<script>
export default {
    name: 'DropsDown',
    props: {
        items: Array
    },
    data: function() {
        return {
            active: -1
        }
    },
    watch: {
        items: function() {
            if (this.active >= this.items.length) {
                this.active = this.items.length - 1;
            }
        }
    },
    methods: {
        selectActive: function()  {
            if (this.active >= 0) {
                this.$emit('selected', this.items[this.active]);
            }
        },
        next: function() {
            if (++this.active >= this.items.length) {
                this.active = 0;
            }
        },
        previous: function() {
            if (--this.active < 0) {
                this.active = this.items.length - 1;
            }
        }
    }
}
</script>

<style scoped>

div {
    margin-bottom: 5px;
}

.dropdown {
    position: absolute;
    background-color: #f9f9f9;
    min-width: 230px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
    text-align: center;
    overflow-y: auto;
    max-height: 350px;
}

span.dropdown-item {
    font-size: 14px;
    font-weight: 400;
    font-style: normal;
    padding: 7px 13px;
    display: block;
    cursor: pointer;
    margin: 3px;
    background-color: #E8EAF6; 
}

span.dropdown-active {
    color: #E8EAF6;
    background-color: #303F9F; 
}

</style>
