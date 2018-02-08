import java.util.*;

public class LRUCache {

	static int cacheSize = 3;

    public static void main(String[] args) {
        System.out.println("LRUCache");

//		myCache = lruCache(cacheSize);
		Map<Integer,String> cache = lruCache(3);
		System.out.println("testing initial cache empty: " + 
			((cache.size() == 0) ? "passed" : " failed" ));
				
		System.out.println("testing get on non-existent key: " + 
			((cache.get(100) == null) ? "passed" : " failed" ));
			
		cache.put(100,"hello world");
		   
		System.out.println("testing get on existent key: " + 
			((cache.get(100) != null) ? "passed" : " failed" ));		
		 
   		cache.put(101, "Operating System");  
   		cache.put(102, "Data Communication and Networking");

		System.out.println("testing cache full: " + 
			((cache.size() == cacheSize) ? "passed" : " failed" ));
   		
   		//making 102 least recently used by accessing others
   		cache.get(100);
   		cache.get(101);
		//insert a new element and confirm 102 is evicted  		
   		cache.put(103, "103");  
//		System.out.println("cache after eviction: "+ cache);
		
		System.out.println("insert a new element and confirm 102 is evicted: " + 
			((cache.get(102) == null) ? "passed" : " failed" ));
		
   		  
   		System.out.println("Values before remove: "+ cache);   

		//if(cache.size() = cacheSize) removeEldestEntry

		String an_entry= cache.get(101);
		cache.put(104, "104");  
		System.out.println("cache after eviction: "+ cache);  
		cache.put(105, "105");  
		cache.put(106, "106");  
		System.out.println("overloading: "+ cache);  
		
		String stale_entry= cache.get(101);
		System.out.println("stale_entry: "+ stale_entry);  
		

    }

	public static Map<Integer,String> lruCache(final int maxSize) {		
    	return new LinkedHashMap<Integer,String>(maxSize, 0.75f, true) {
        	@Override
        	protected boolean removeEldestEntry(Map.Entry<Integer,String> eldest) {
            	return size() > maxSize;
        	}
        	
   		};
	}

}
