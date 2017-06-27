<template>
    <div class="cs-card mdl-shadow--4dp mdl-cell cs-card--faded">
        <a v-if="href" :href="href" class="cs-card__link">
            <i v-if="icon" class="material-design-icon cs-card__icon">{{ icon }}</i>
        </a>
        <span v-if="!href">
            <i v-if="icon" class="material-design-icon cs-card__icon">{{ icon }}</i>
        </span>

        <h1 class="cs-card__title">{{ title }}</h1>
        <p>{{ text }}</p>
    </div>
</template>


<script>
module.exports = {
    data: function() {
        return {
            title: 'test title',
            text: 'sample text'
            href: null,
            icon: 'do_not_disturb',
        }
    }
}
</script>


<style lang="sass" scoped>
.cs-card {
    @include block-padding;
    @extend .mdl-cell--6-col;
    @extend .mdl-cell--12-col-tablet;

    display: flex;
    background-color: white;
    min-height: 100px;
    color: $color-dark-gray;
    vertical-align: center;

    &__title {
        @include title-emph;
    }

    &__content {
        margin-top: $small-spacing;
    }

    &__icon {
        @include icon-big;
        margin-right: $large-spacing;
    }

    &__link {
        display: block;
        text-decoration: none;
    }

    &--faded {
        background-color: rgba(220, 220, 220, 170);
    }
}

@media only screen and (min-width: $breakpoint-medium-screen) {
    .cs-card {
        display: block;
        text-align: center;

        &__icon {
            margin-right: inherit;
        }
    }
}
</style>