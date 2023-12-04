module Jekyll
  module TOUTC
    def to_utc(stamp)
      time(stamp).utc
    end
  end
end

Liquid::Template.register_filter(Jekyll::TOUTC)
