        function p(e) {
            for (var t = 1; t < arguments.length; t++) {
                var n = null != arguments[t] ? arguments[t] : {}
                  , r = s()(n);
                "function" == typeof a.a && (r = r.concat(a()(n).filter(function(e) {
                    return o()(n, e).enumerable
                }))),
                r.forEach(function(t) {
                    f(e, t, n[t])
                })
            }
            return e
        }