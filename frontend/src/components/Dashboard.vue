<template>
    <div id="dashboard">
        <div class="dashboard-float-right">
            <a href="javascript:void(0)"  @click="logout">Logout</a>
        </div>
        <div class="dashboard-float-left">
            <template v-if="state === 'PROTOCOL_ADD'">
                <a href="javascript:void(0)" class="symbol" @click="goback">Zur&uuml;ck</a>
            </template>
            <template v-else-if="state === 'PROTOCOL_LOAD'">
                <a href="javascript:void(0)" class="symbol" @click="goback">Zur&uuml;ck</a>
            </template>
            <template v-else-if="state === 'MAIN_MENU'">
                <a href="javascript:void(0)" @click="protocolAdd">Neu</a>
                <a href="javascript:void(0)" @click="protocolLoad">Laden</a>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Dashboard',
    props: {
        value: String,
    },
    data: function() {
        return {};
    },
    computed: {
        state: function() { return this.value; }
    },
    methods: {
        goback: function() {
            this.setState('MAIN_MENU');
        },
        protocolAdd: function() {
            this.setState('PROTOCOL_ADD');
        },
        protocolLoad: function() {
            this.setState('PROTOCOL_LOAD');
        },
        logout: function() {
            console.log('WHOOHOOHOOO easy there..');
        },
        setState: function(newVal) {
            this.$emit('input', newVal);
        }
    }
}
</script>

<style scoped>

div#dashboard {
    position: fixed;
    width: 100%;
    z-index: 9999;
    margin: 0px;
    top: 0;
    left: 0;
}

#dashboard {
    background: #303F9F;
    height: 63px;
    text-align: center;
}

#dashboard a {
    color: #E8EAF6;
    text-decoration: none;
    font-style: italic;
    font-size: 20px;
    font-weight: bold;
    padding: 9px;
    margin-left: 3px;
}

#dashboard a:hover {
    color: #303F9F;
    background: #E8EAF6;
}

.dashboard-float-right {
    float: right;
    margin-right: 5px;
    position: relative;
    top: 30%;
}

.dashboard-float-left {
    float: left;
    margin-left: 5px;
    position: relative;
    top: 30%;
}

</style>