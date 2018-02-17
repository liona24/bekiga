<template>
    <div class="preview">
        <loader v-if="isLoading" size="20"></loader>
        <template v-else>
            <p>{{ props.name }}</p>
            <p>{{ props.street }}</p>
            <p>{{ props.zipCode }} {{ props.city }}</p>
            <p> TODO: PICTURE </p>
        </template>
    </div>
</template>

<script>
import Loader from './Loader'

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
                name: '',
                street: '',
                zipCode: '',
                city: '',
                picture: '',
            }
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

<style>

</style>