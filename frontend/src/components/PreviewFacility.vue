<template>
    <div class="preview">
        <loader v-if="isLoading" size="20"></loader>
        <template v-else>
            <p>{{ props.name }}</p>
            <p>{{ props.street }}</p>
            <p>{{ props.zipCode }} {{ props.city }}</p>
            <img v-if="props.picture" :src="imgSrc">
        </template>
    </div>
</template>

<script>
import Loader from './Loader'

import { urlApi } from '../urls.js'
import { getFacility } from '../ajax.js'

export default {
    name: 'PreviewFacility',
    components: {
        Loader,
    },
    props: {
        data: Object
    },
    data: function() {
        return {
            isLoading: true,
            props: {
                _id: '',
                name: '',
                street: '',
                zipCode: '',
                city: '',
                picture: '',
            }
        }
    },
    computed: {
        imgSrc: function() {
            return urlApi + 'files/?_id=facility_' + this.props._id + '.' + this.props.picture
        }
    },
    created: function() {
        this.isLoading = true;

        if (this.data) {
            getFacility(this.data._id).then((res) => {
                this.props = res.data;
                this.isLoading = false;
            }, (result) => console.log(result));
        }
    },
}
</script>

<style scoped>

img {
    width: 180px;
    height: 140px;
    margin-left: -80px;
    position: relative;
    left: 50%;
    float: none;
}
</style>