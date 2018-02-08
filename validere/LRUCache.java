import java.util.*;

public class LRUCache {

	static int cacheSize = 3;

    public static void main(String[] args) {
        System.out.println("LRUCache");

//		myCache = lruCache(cacheSize);
		LinkedHashMap<Integer,Integer> myCache = lruCache(3);
		System.out.println(myCache.size());

    }

	public static <K,V> Map<K,V> lruCache(final int maxSize) {
		System.out.println("lruCache");
    	return new LinkedHashMap<K, V>(maxSize*4/3, 0.75f, true) {
        	@Override
        	protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
            	return size() > maxSize;
        	}
   		};
	}

}
