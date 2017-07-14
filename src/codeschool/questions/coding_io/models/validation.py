
class Validation():
    """
    This class is responsible for validation
    """

    def schedule_validation(self):
        """
        Schedule full validation to be performed in the background.

        This executes the full_clean_code() method
        """

        print('scheduling full code validation... (we are now executing on the'
              'foreground).')

    def validate_tests(self):
        """
        Triggered when (pre|post)_test_source changes or on the first time the
        .clean() method is called.
        """

        # Check if new source is valid
        for attr in ['pre_tests_source', 'post_tests_source']:
            try:
                source = getattr(self, attr)
                if source:
                    iospec = parse_iospec(source)
                else:
                    iospec = None
                setattr(self, attr[:-7], iospec)
            except Exception as ex:
                self.clear_tests()
                raise ValidationError(
                    {attr: _('invalid iospec syntax: %s' % ex)}
                )

        # Computes temporary expansions for all sources. A second step may be
        # required in which we use the reference source in answer key to further
        # expand iospec data structures
        iospec = self.pre_tests.copy()
        iospec.expand_inputs(self.number_of_pre_expansions)
        self.pre_tests_expanded = iospec

        if self.pre_tests_source and self.post_tests_source:
            iospec = ejudge.combine_iospecs(self.pre_tests, self.post_tests)
        elif self.post_tests_source:
            iospec = self.post_tests.copy()
        elif self.pre_tests_source:
            iospec = self.pre_tests.copy()
        else:
            raise ValidationError(_(
                'either pre_tests_source or post_tests_source must be given!'
            ))
        iospec.expand_inputs(self.number_of_post_expansions)
        # assert len(iospec) >= self.number_of_expansions, iospec
        self.post_tests_expanded = iospec

        if self.pre_tests_expanded.is_expanded and \
                self.post_tests_expanded.is_expanded:
            self.pre_tests_expanded_source = self.pre_tests_expanded.source()
            self.post_tests_expanded_source = self.post_tests_expanded.source()

        else:
            self._expand_from_answer_keys()

        # Iospec is valid: save the hash
        self.tests_state_hash = self.current_tests_hash

    def _expand_from_answer_keys(self):
        # If the source requires expansion, we have to check all answer keys
        # to see if one of them defines a valid source and compute the expansion
        # from this source. All languages must produce the same expansion,
        # otherwise it is considered to be an error.
        #
        # If no answer key is available, leave pre_tests_expanded_source blank
        assert self.pre_tests_expanded is not None
        assert self.post_tests_expanded is not None
        pre, post = self.pre_tests_expanded, self.post_tests_expanded

        useful_keys = list(self.answers_with_code())
        if useful_keys:
            ex_pre = pre.copy()
            ex_pre.expand_inputs(self.number_of_pre_expansions)
            ex_post = post.copy()
            ex_post.expand_inputs(self.number_of_post_expansions)
            pre_list = self.answers.expand_all(ex_pre)
            post_list = self.answers.expand_all(ex_post)

            if len(pre_list) == len(post_list) == 1:
                ex_pre = pre_list[0]
                ex_post = post_list[0]
            else:
                def validate(L, field):
                    first, *tail = L
                    for i, elem in enumerate(tail, 1):
                        if first == elem:
                            continue

                        lang1 = useful_keys[0].language
                        lang2 = useful_keys[i].language
                        first.language = lang1
                        elem.language = lang2
                        self.clear_tests()
                        raise validators.inconsistent_testcase_error(first,
                                                                     elem,
                                                                     field)

                validate(pre_list, 'pre_tests_expanded_source')
                validate(post_list, 'post_tests_expanded_source')
                ex_pre, ex_post = pre_list[0], post_list[0]

            # Update values
            self.pre_tests_expanded = ex_pre
            self.pre_tests_expanded_source = ex_pre.source()
            self.post_tests_expanded = ex_pre
            self.post_tests_expanded_source = ex_post.source()
