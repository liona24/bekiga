<template>
    <div class="preview">
        <loader v-if="isLoading" size="20"></loader>
        <template v-else>
            <p>{{ props.name }}</p>
        </template>
    </div>
</template>

<script>
import Loader from './Loader'

import { getInspectionStandard } from '../ajax.js'

export default {
    name: 'PreviewInspectionStandard',
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
            }
        }
    },
    created: function() {
        this.isLoading = true;

        if (this.data) {
            getInspectionStandard(this.data._id).then((res) => {
                this.props = res.data;
                this.isLoading = false;
            }, (result) => console.error(result));
        }
    },
}
</script>

<style>

</style>