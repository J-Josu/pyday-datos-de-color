<div class="flex flex-col gap-8 [&>p]:font-bold">
  <slot />
</div>

<style lang="postcss">
  div :global(h2) {
    @apply text-6xl font-bold text-stone-100;
  }
  div :global(p) {
    @apply text-stone-200;
  }

  div :global(small) {
    @apply text-stone-300 font-medium;
  }
</style>
