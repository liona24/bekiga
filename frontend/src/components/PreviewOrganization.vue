<template>
    <div class="preview">
        <loader v-if="isLoading" size="20"></loader>
        <template v-else>
            <p>{{ props.name }}</p>
            <p>{{ props.street }}</p>
            <p>{{ props.zipCode }} {{ props.city }}</p>
        </template>
    </div>
</template>

<script>
import Loader from './Loader'

import { getOrganization } from '../ajax.js'

export default {
    name: 'PreviewOrganization',
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
                city: ''
            }
        }
    },
    created: function() {
        this.isLoading = true;

        if (this.data) {
            getOrganization(this.data._id).then((org) => {
                this.props = org.data;
                this.isLoading = false;
            }, (result) => console.log(result));
        }
    },
}
</script>

<style>

</style>